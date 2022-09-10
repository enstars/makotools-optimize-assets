
# drive -> local
rclone copy "RaisDrive:/Enstars2/Shared/frameless cards" assets
rclone copy "RaisDrive:/Enstars2/Shared/cgs" assets
rclone copy "RaisDrive:/Enstars2/Shared/renders" assets
# WARNING: Don't use rclone sync as it may delete files already on there

# convert image
bash png2jpg.sh assets 90
bash png2webp.sh assets 90

# optimize images
bash optimize-jpg.sh assets 95

# combined
bash png2jpg.sh assets 90 && bash png2webp.sh assets 90 && bash optimize-jpg.sh assets 95

# local -> backblaze
rclone copy assets "Backblaze:ensemble-square/assets"

# others

rclone copy "Backblaze:ensemble-square/render" render
bash png2jpg.sh render 90 && bash png2webp.sh render 90 && bash optimize-jpg.sh render 95
rclone copy render "Backblaze:ensemble-square/render" 