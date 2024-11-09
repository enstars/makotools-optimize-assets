
# drive -> local
rclone copy "RaisDrive:enstars transparents/Enstars2/Shared/frameless cards" assets
rclone copy "RaisDrive:enstars transparents/Enstars2/Shared/cgs" assets
rclone copy "RaisDrive:enstars transparents/Enstars2/Shared/renders" assets
# WARNING: Don't use rclone sync as it may delete files already on there

# get files from backblaze directly (not recommended / not for updating)
# rclone copy "Backblaze:ensemble-square/assets" assets

# fix renders
bash removeRenderArtifacts.sh assets

# convert image
bash png2jpg.sh assets 90
bash png2webp.sh assets 90

# optimize images
bash optimize-jpg.sh assets 95

# combined
bash removeRenderArtifacts.sh assets && bash png2jpg.sh assets 90 && bash png2webp.sh assets 90 && bash optimize-jpg.sh assets 95

# local -> backblaze
rclone copy assets "Backblaze:ensemble-square/assets"
