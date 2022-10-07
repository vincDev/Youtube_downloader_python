import youtube_downloader_script

print("")
print("--------------------------------")
print("BIENVENUE SUR YOUTUBE_DOWNLOADER")
print("--------------------------------")
print("")

url = youtube_downloader_script.get_video_url_from_user()
youtube_downloader_script.download_video(url)