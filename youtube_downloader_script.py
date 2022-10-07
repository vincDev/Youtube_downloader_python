# projet youtube downloader

# installer module pytube
from pytube import YouTube
import ffmpeg
import os

BASE_YOUTUBE_URL = "https://www.youtube.com/"

# demander l'url
def get_video_url_from_user():
    # verifier que l'url commence par https://www.youtube.com/
    url = input("Entrer l'url de la vidéo :\n")
    if url.lower().startswith(BASE_YOUTUBE_URL):
        return url
    print("ERROR : Entrez une URL youtube")
    return get_video_url_from_user()
    
    
# demander le choix de la résolution
# def get_video_stream_itag_from_user(streams):
#     print("")
#     print("Choix des résolutions :")
#     index = 1
#     for stream in streams:
#         print(f"    {index}- {stream.resolution}")
#         index += 1

#     while(True):
#         number_choice = input("choisissez la résolution : ")
#         if number_choice == "":
#             print("ERROR: Vous devez rentrer un nombre")
#         else:
#             try:
#                 number_choice_int =  int(number_choice)
#             except:
#                 print("ERROR: Vous devez rentrer un nombre")
#             else:
#                 if not 1<= number_choice_int <= len(streams):
#                     print(f"ERROR: Vous devez rentrer un nombre entre 1 et {len(streams)}")
#                 else:
#                     break
                    
#     itag = streams[number_choice_int-1].itag
#     res_selected = streams[number_choice_int-1].resolution
#     return itag, res_selected

# afficher la progression
def on_download_progress(stream, chunk, bytes_remaining):
    bytes_downloaded = stream.filesize - bytes_remaining
    percent = bytes_downloaded * 100 / stream.filesize
    print(f"Progression du téléchargement : {int(percent)} %")


#----------------------- début du programme principal --------------------------------
# url = "https://www.youtube.com/watch?v=UCskpE9KGQU"
# url = "https://www.youtube.com/watch?v=9bZkp7q19f0"
# url = "https://www.youtube.com/watch?v=pAgnJDJN4VA"
# url = "https://www.youtube.com/watch?v=kp1QxuX1nPI"
# url = get_video_url_from_user()

def download_video(url):

    # création de l'objet youtube contenant les infos de la video via l'url
    youtube_video = YouTube(url)
    youtube_video.register_on_progress_callback(on_download_progress) # fonction callback a chaque evolution de telechargement

    # print(f"Titre : {youtube_video.title}")
    # print(f"nb vues : {youtube_video.views}")

    streams = youtube_video.streams.filter(progressive=False, file_extension="mp4", type="video").order_by("resolution").desc()

    video_stream = youtube_video.streams.get_by_itag(137)
    streams = youtube_video.streams.filter(progressive=False, file_extension="mp4", type="audio").order_by("abr").desc()
    audio_stream = streams[0]
    # print(f"video stream : {video_stream}")
    # print(f"audio stream : {audio_stream}")


    # partie du téléchargement

    # stream = youtube_video.streams.get_by_itag(18)
    ok = input(f"Voulez-vous télécharger {youtube_video.title} ? y/n : ")
    if ok == "n":
        url = get_video_url_from_user()
        download_video(url)
    # stream = youtube_video.streams.get_highest_resolution()
    # stream = youtube_video.streams.get_by_itag(140);
    print(f"TÉLÉCHARGEMENT DE {youtube_video.title} ...")
    video_stream.download("video")
    audio_stream.download("audio")

    audio_filename = os.path.join("audio", video_stream.default_filename)
    video_filename = os.path.join("video", video_stream.default_filename)
    output_filename = os.path.join("Desktop",video_stream.default_filename)
    # print("Combinaison des fichiers ...")
    ffmpeg.output(ffmpeg.input(audio_filename), ffmpeg.input(video_filename), output_filename, vcodec="copy", acodec="copy", loglevel="quiet").run(overwrite_output=True)
    print("OK")
    
    os.remove(audio_filename)
    os.remove(video_filename)
    os.rmdir("audio")
    os.rmdir("video")


    