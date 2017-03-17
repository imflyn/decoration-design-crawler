import shutil

from config import mongodb, IMAGES_STORE

from msic.config import redis_client

mongodb.drop_collection("design_picture")
mongodb.drop_collection("design_picture_summary")
mongodb.drop_collection("design_topic")

redis_client.delete('tubatu_design_topic_filter')
redis_client.delete('tubatu_design_picture_filter')

shutil.rmtree(IMAGES_STORE)
