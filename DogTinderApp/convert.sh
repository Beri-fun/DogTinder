path=$(pwd)
path1="/DogTinderApp/static/audio.wav"
path2="/DogTinderApp/static/output.wav"
pathstart="$path$path1"
pathfinish="$path$path2"
ffmpeg -i $pathstart -ar 16000 -ac 1 -sample_fmt s16 $pathfinish -loglevel quiet