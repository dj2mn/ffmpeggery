### crop lower left quadrant
`ffmpeg -i input.mp4 -filter:v "crop=iw*(5/10):ih*(5/10):0:ih" output.mp4`

----

### crop upper right quadrant
`ffmpeg -i input.mp4 -filter:v "crop=iw*(5/10):ih*(5/10):iw:0" output.mp4`

----

### copy audio track only
`ffmpeg -i input.mp4 -vn -c:a copy output.mp4`

----

### the concatenate one-liner 
`ffmpeg -f concat -safe 0 -i <(for f in *.mp4; do echo "file '$PWD/$f'"; done) -c copy output.mp4`

----

### something very specific I did once
`ffmpeg -r 15 -pattern_type glob -i '*.JPG' -vf "scale=1920:-1" -vcodec libx264 -preset veryslow -crf 15 -pix_fmt yuv420p Timelapse1.mp4`

----

### convert all MOV files to mp4 and keep file datetimes
`for file in *.MOV ; do ffmpeg -y -i "$file" "${file%.*}.mp4" ; touch -r "$file" "${file%.*}.mp4" ; done`

----

### pillarbox a portrait video
`ffmpeg -i input.mp4 -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:-1:-1:color=black" output.mp4`

----

### change frame rate
 - with re-encoding:<br />
`ffmpeg -i input.mp4 -vf "setpts=1.25*PTS" -r 24 output.mp4`
 - without re-encoding:
   1. extract video to raw bitstream,<br />
      `ffmpeg -i input.mp4 -c copy -f h264 input.h264`
   2. remux with new framerate<br />
      `ffmpeg -r 24 -i input.h264 -c copy output.mp4`

----

### resize anything to 1280x720 with auto letterbox
[(source: superuser)](https://superuser.com/questions/891145/ffmpeg-upscale-and-letterbox-a-video)

`ffmpeg -i input.mp4 -vf = "scale=(iw*sar)*min(1280/(iw*sar)\,720/ih):ih*min(1280/(iw*sar)\,720/ih), pad=1280:720:(1280-iw*min(1280/iw\,720/ih))/2:(720-ih*min(1280/iw\,720/ih))/2" output.mp4`

