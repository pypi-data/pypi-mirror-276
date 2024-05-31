from src.openi import *

test_file = "test/chatglm/pytorch_model-00001-of-00008.bin"
# f = LocalFile(test_file)
# print(f)
# print(f"name: {f.name}")
# print(f"size: {f.size}")
# print(f"total_chunks_count: {f.total_chunks_count}")
# print(f"md5: {f.md5()}")
# print(f"md5 model: {f.md5('model')}")
#
# import time
#
# with f.tqdm_stream_file_by_chunk() as f_stream:
#     for n, d in f_stream:
#         time.sleep(0.1)
test_folder = "test/upload"

test_file2 = "test/upload/100M.zip"
small_file = "test/text.txt"

# upload_model_file(repo_id="chenzh01/randomrepo", model_name="chatglm3",
#                   file=test_file2)

# upload_model(repo_id="chenzh01/randomrepo", model_name="randomf",
#              folder=test_folder, create_model=True)
download_model_file(repo_id="chenzh01/randomrepo", model_name="randomf",
                    filename="100M.zip",
                    save_path="test/download")
