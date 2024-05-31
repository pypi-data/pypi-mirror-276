from src.openi import *


def test_api_class(resp):
    print(resp)
    print()
    for k, v in resp.__dict__.items():
        print(f"{k} = {v}")


def generate_dataclass(resp):
    jprint(resp)
    for k, v in resp.items():
        print(f"{k}: Optional[{type(v).__name__}]")


def hf_get_file_link(hf_model_repo_id: str = "THUDM/chatglm3-6b"):
    hf_model_files_with_urls = []

    hf_model_files = hf_api.list_repo_tree(
        hf_model_repo_id
    )  # list_files_info,list_repo_files
    for file in hf_model_files:
        print(file)
    #     data = file.rfilename + file.blob_id
    #     hf_openi_md5 = md5(data.encode("utf-8")).hexdigest()

    #     name = file.rfilename
    #     size = file.size

    #     hf_url = hf_hub_url(repo_id=hf_model_repo_id, filename=file.rfilename)
    #     download_url = get_hf_file_metadata(hf_url).location

    #     file_obj = dict(
    #         name=name,
    #         size=size,
    #         hf_url=hf_url,
    #         download_url=download_url,
    #         md5=hf_openi_md5,
    #     )
    #     hf_model_files_with_urls.append(file_obj)
    # print(hf_model_files_with_urls)
    #
    # r = requests.get(download_url, stream=True)
    # for chunk in r.iter_content(chunk_size=chunk_size):
    #     print(chunk)


def upload_to_openi_model(
        file: object,
        model_id: str,
        repo_id: str,
        chunk_size: int = 1024 * 1024 * 64,
        cluster: str = "NPU",
):
    local_path = file.path
    file_name = file.name
    size = file.size
    md5 = calculate_file_md5(local_path)
    model_id = model_id

    max_width = 15
    if len(file_name) > max_width:
        title = "…" + file_name[-1 * max_width:]
    else:
        title = file_name.rjust(max_width + 1)
    bar_format = (
        "{desc}{percentage:3.0f}%|{bar}| "
        "{n_fmt}{unit}/{total_fmt}{unit} "
        "[{elapsed}<{remaining}, "
        "{rate_fmt}{postfix}]"
    )
    desc = f"{title}: "
    pbar = tqdm(
        total=size,
        leave=True,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
        bar_format=bar_format,
        desc=desc,
        colour="green",
    )

    upload_type = UPLOAD_TYPE_TO_INT[cluster.upper()]
    total_chunks_counts = math.ceil(size / chunk_size)

    get_chunks = api.upload_get_chunks(
        dataset_or_model_id=model_id,
        filename=file_name,
        md5=md5,
        upload_type=upload_type,
        upload_mode="model",
    )
    logger.info(get_chunks)

    if get_chunks.uploaded:
        model_url = openi_api.get_model_url(
            repo_id=repo_id, model_name=get_chunks.dataset_or_model_name
        )
        pbar.set_description_str(f"already uploaded, skip {desc}")
        logger.info(f"✔ already uploaded, view in {model_url}")
    else:
        uuid, upload_id = get_chunks.uuid, get_chunks.uploadID
        if not uuid or not upload_id:
            new_multipart = api.model_new_multipart(
                modeluuid=model_id,
                filename=file_name,
                upload_type=upload_type,
                md5=md5,
                filesize=size,
                total_chunks_counts=total_chunks_counts,
            )
            uuid = new_multipart.uuid
            upload_id = new_multipart.uploadID

        uploaded_chunks = get_chunks.uploaded_chunks
        file_chunks = [
            i for i in range(1, total_chunks_counts + 1) if i not in uploaded_chunks
        ]
        failed_chunks = []
        pbar.update(len(uploaded_chunks) * chunk_size)
        # print(uuid, upload_id, file_chunks)

        for chunk in file_chunks:
            if chunk not in file_chunks:
                chunk += 1
                tqdm.write(f"skip chunk {chunk}")
                continue

            multipart_url = openi_api.model_get_multipart_url(
                uuid=uuid,
                upload_type=upload_type,
                upload_id=upload_id,
                chunk_number=chunk,
                chunk_size=chunk_size,
            )
            if multipart_url.url:
                f_index = (chunk - 1) * chunk_size
                upload_data = read_file_by_chunk(local_path, f_index, chunk_size)
                etag = api.openi_file_upload(
                    url=multipart_url.url,
                    filedata=upload_data,
                    upload_type=upload_type,
                )
                if etag:
                    pbar.update(len(upload_data))
                    logger.info(
                        f"✔ /put_upload {chunk} data len {len(upload_data)} etag {etag}"
                    )
                else:
                    logger.info(f"🚫 /put_upload {chunk}")
                    failed_chunks.append(chunk)

            else:
                logger.info(f"🚫 /model_get_multipart_url {chunk}")
                failed_chunks.append(chunk)
            chunk += 1

        if not failed_chunks:
            complete = openi_api.model_complete_multipart(
                modeluuid=model_id,
                upload_type=upload_type,
                uuid=uuid,
                upload_id=upload_id,
            )
            if complete:
                logger.info("✔ /model_complete_multipart")
            else:
                logger.info("🚫 /model_complete_multipart")
        else:
            logger.info(f"🚫 upload failed_chunks {failed_chunks}")


model_dir = "/Users/jochen10518/Documents/project/pcl/openi-test/model1"


# files = list_files_in_directory(model_dir)
# model = openi_api.get_model("chenzh01/llms", "model2")
# model_id = model[0]["id"]
# for f in files:
#     upload_to_openi_model(
#         file=f,
#         model_id=model_id,
#         repo_id="chenzh01/llms",
#         cluster="npu",
#     )


def _prepare_upload_folder_additions(
        folder_path: Union[str, Path],
        path_in_repo: str = None,
        allow_patterns: Optional[Union[List[str], str]] = None,
        ignore_patterns: Optional[Union[List[str], str]] = None,
):
    """Generate the list of Add operations for a commit to upload a folder.

    Files not matching the `allow_patterns` (allowlist) and `ignore_patterns` (denylist)
    constraints are discarded.
    """
    folder_path = Path(folder_path).expanduser().resolve()
    if not folder_path.is_dir():
        raise ValueError(f"Provided path: '{folder_path}' is not a directory")

    # List files from folder
    relpath_to_abspath = {
        path.relative_to(folder_path).as_posix(): path
        for path in sorted(folder_path.glob("**/*"))  # sorted to be deterministic
        if path.is_file()
    }
    for k, v in relpath_to_abspath.items():
        print(k)
        print(v)
        print()

    # # Filter files and return
    # # Patterns are applied on the path relative to `folder_path`. `path_in_repo` is prefixed after the filtering.
    prefix = f"{path_in_repo.strip('/')}/" if path_in_repo else ""
    print(prefix)
    # return [
    #     CommitOperationAdd(
    #         path_or_fileobj=relpath_to_abspath[relpath],  # absolute path on disk
    #         path_in_repo=prefix + relpath,  # "absolute" path in repo
    #     )
    #     for relpath in filter_repo_objects(
    #         relpath_to_abspath.keys(),
    #         allow_patterns=allow_patterns,
    #         ignore_patterns=ignore_patterns,
    #     )
    # ]

# _prepare_upload_folder_additions(model_dir)
