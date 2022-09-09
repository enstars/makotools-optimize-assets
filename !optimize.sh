
# drive -> local
rclone copy "RaisDrive:/Enstars2/Shared/frameless cards" assets
# WARNING: Don't use rclone sync as it may delete files already on there

# convert image
bash png2jpg.sh assets 90
bash png2webp.sh assets 90

# optimize images
bash optimize-jpg.sh assets 95

# local -> backblaze
rclone copy assets "Backblaze:ensemble-square/assets"