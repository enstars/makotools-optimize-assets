from rclone_python import rclone
import subprocess
import os
from wand.image import Image
from glob import glob


def rclone_check(query: str, output_file: str, src: str):
    file_exclusion = "*.{jpg, jpeg, webp}"

    if os.path.exists(output_file) == False:
        try:
            print("Fetching new images")
            subprocess.run(
                f"rclone check '{src}' 'backblaze:ensemble-square/assets' --include '{query}' --exclude '{file_exclusion}' --one-way --missing-on-dst {output_file}",
                shell=True,
                text=True,
            )
        except:
            print("Finished")
    else:
        print(f"{output_file} already exists, skipping")


def rclone_copyto(file: str, src: str, dest: str):
    if os.path.exists(file):
        print(f"Copying {file} onto device")
        with open(file, "r+") as image_files:
            for file in image_files:
                file = file.replace("\n", "")
                rclone.copyto(
                    src + "/" + file,
                    dest + "/" + file,
                    ignore_existing=False,
                    show_progress=True,
                )
    else:
        print(f"There is no {file}, skipping")


def rclone_upload(src: str, dest: str):
    try:
        rclone.copy(src, dest, show_progress=True)
    except:
        print("Could not upload files")


def remove_render_artifacts(assets_location: str):
    # i have no clue what this does
    png_files = glob(assets_location + "/card_full1*.png")
    for file in png_files:
        try:
            print(f"Removing render artifacts from {file}")
            os.system(
                f"magick '{file}' \( -clone 0 -channel a -fx 0 \) \( -clone 0  -alpha extract -channel RGB -black-threshold 5% +channel  \) -swap 0,1 -composite '{file}'"
            )
        except:
            print(f"Could not remove artifacts from {file}, skipping")


def png2jpg(assets_location: str):
    png_files = glob(assets_location + "/card_full1*.png")
    for file in png_files:
        with Image(filename=file) as png:
            print(f"Opening {file} to convert to jpeg")
            with png.convert("jpeg") as jpeg:
                print(f"{file} converted to jpeg")
                jpeg.compression_quality = 90
                jpeg_filename = file.split(".")[0] + ".jpeg"
                jpeg.save(filename=jpeg_filename)
                if os.path.exists(jpeg_filename):
                    print(f"{jpeg_filename} saved successfully")
                else:
                    print(f"{jpeg_filename} was not saved :(")


def png2webp(assets_location: str):
    png_files = glob(assets_location + "/*.png")
    for file in png_files:
        try:
            print(f"Converting {file} to webp")
            webp_filename = file.split(".")[0] + ".webp"
            os.system(f"cwebp '{file}' -q 90 -o '{webp_filename}'")
            if os.path.exists(webp_filename):
                print(f"{webp_filename} saved successfully")
            else:
                print(f"{webp_filename} was not saved")
        except:
            print(f"Could not convert {file} to a webp, skipping")
            continue


def optimize_jpegs(assets_location: str):
    jpeg_files = glob(assets_location + "/*.jpeg")
    for file in jpeg_files:
        try:
            print(f"Optimizing {file}")
            os.system(f"jpegoptim -m 95 '{file}'")
        except:
            print(f"Could not optimize {file}, skipping")
            continue

        with Image(filename=file) as jpeg:
            jpeg.resize(10, 10)
            jpeg.save(filename=file.replace(".jpeg", "-placeholder.jpeg"))


if __name__ == "__main__":
    if rclone.is_installed() == False:
        raise Exception("Rclone is not installed, please install it!")

    os.system("mkdir assets")

    # get files that are on the assets drive but not on mktls
    if rclone.check_remote_existing("RaisDrive") == False:
        raise Exception("Rai's drive is not on your system")

    ONEDRIVE_FRAMELESS = (
        "RaisDrive:enstars transparents/Enstars2/Shared/frameless cards"
    )
    ONEDRIVE_CGS = "RaisDrive:enstars transparents/Enstars2/Shared/cgs"
    ONEDRIVE_RENDERS = "RaisDrive:enstars transparents/Enstars2/Shared/renders"
    ONEDRIVE_CHARACTERS = (
        "RaisDrive:enstars transparents/Enstars Fullbody Renders (Game)"
    )
    ONEDRIVE_KR_CGS = "RaisDrive:enstars transparents/Enstars2/Foreign Exclusive/KR/cgs"
    ONEDRIVE_KR_FRAMELESS = (
        "RaisDrive:enstars transparents/Enstars2/Foreign Exclusive/KR/frameless"
    )
    ONEDRIVE_KR_RENDERS = (
        "RaisDrive:enstars transparents/Enstars2/Foreign Exclusive/KR/renders"
    )
    ONEDRIVE_GLOBAL_FRAMELESS = (
        "RaisDrive:enstars transparents/Enstars2/Foreign Exclusive/Shared/frameless"
    )
    ONEDRIVE_GLOBAL_CGS = (
        "RaisDrive:enstars transparents/Enstars2/Foreign Exclusive/Shared/cgs"
    )
    ONEDRIVE_GLOBAL_RENDERS = (
        "RaisDrive:enstars transparents/Enstars2/Foreign Exclusive/Shared/renders"
    )

    FRAMELESS_OUTPUT = "missing_frameless.txt"
    CGS_OUTPUT = "missing_cgs.txt"
    RENDERS_OUTPUT = "missing_renders.txt"
    CHARAS_OUTPUT = "missing_charas.txt"
    KR_CGS_OUTPUT = "missing_kr_cgs.txt"
    KR_FRAMELESS_OUTPUT = "missing_kr_frameless.txt"
    KR_RENDERS_OUTPUT = "missing_kr_renders.txt"
    GLOBAL_CGS_OUTPUT = "missing_global_cgs.txt"
    GLOBAL_FRAMELESS_OUTPUT = "missing_global_frameless.txt"
    GLOBAL_RENDERS_OUTPUT = "missing_global_renders.txt"

    FRAMELESS_QUERY = "card_rectangle4_*.png"
    CG_QUERY = "card_still_full1_*.png"
    RENDER_QUERY = "card_full1_*.png"
    CHARA_QUERY = "character_full1_*.png"

    rclone_check(FRAMELESS_QUERY, FRAMELESS_OUTPUT, ONEDRIVE_FRAMELESS)
    rclone_check(CG_QUERY, CGS_OUTPUT, ONEDRIVE_CGS)
    rclone_check(RENDER_QUERY, RENDERS_OUTPUT, ONEDRIVE_RENDERS)
    rclone_check(CHARA_QUERY, CHARAS_OUTPUT, ONEDRIVE_CHARACTERS)
    rclone_check(CG_QUERY, KR_CGS_OUTPUT, ONEDRIVE_KR_CGS)
    rclone_check(FRAMELESS_QUERY, KR_FRAMELESS_OUTPUT, ONEDRIVE_KR_FRAMELESS)
    rclone_check(RENDER_QUERY, KR_RENDERS_OUTPUT, ONEDRIVE_KR_RENDERS)
    rclone_check(CG_QUERY, GLOBAL_CGS_OUTPUT, ONEDRIVE_GLOBAL_CGS)
    rclone_check(FRAMELESS_QUERY, GLOBAL_FRAMELESS_OUTPUT, ONEDRIVE_GLOBAL_FRAMELESS)
    rclone_check(RENDER_QUERY, GLOBAL_RENDERS_OUTPUT, ONEDRIVE_GLOBAL_RENDERS)

    # now that missing files are here, copy them to your computer
    assets_path = os.getcwd() + "/assets"

    print(f"does assets dir exist: {os.path.exists(assets_path)}")

    rclone_copyto(
        FRAMELESS_OUTPUT,
        ONEDRIVE_FRAMELESS,
        assets_path,
    )
    rclone_copyto(
        CGS_OUTPUT,
        ONEDRIVE_CGS,
        assets_path,
    )
    rclone_copyto(RENDERS_OUTPUT, ONEDRIVE_RENDERS, assets_path)
    rclone_copyto(CHARAS_OUTPUT, ONEDRIVE_CHARACTERS, assets_path)
    rclone_copyto(KR_CGS_OUTPUT, ONEDRIVE_KR_CGS, assets_path)
    rclone_copyto(KR_FRAMELESS_OUTPUT, ONEDRIVE_KR_FRAMELESS, assets_path)
    rclone_copyto(KR_RENDERS_OUTPUT, ONEDRIVE_KR_RENDERS, assets_path)
    rclone_copyto(GLOBAL_CGS_OUTPUT, ONEDRIVE_GLOBAL_CGS, assets_path)
    rclone_copyto(GLOBAL_RENDERS_OUTPUT, ONEDRIVE_GLOBAL_RENDERS, assets_path)
    rclone_copyto(GLOBAL_FRAMELESS_OUTPUT, ONEDRIVE_GLOBAL_FRAMELESS, assets_path)

    # optimize and convert images before uploading them
    remove_render_artifacts(assets_path)
    png2jpg(assets_path)
    png2webp(assets_path)
    optimize_jpegs(assets_path)

    # upload the images to backblaze
    rclone_upload(assets_path, "backblaze:ensemble-square/assets")

    # delete files and assets
    os.system(
        f"rm {FRAMELESS_OUTPUT} {RENDERS_OUTPUT} {CGS_OUTPUT} {CHARAS_OUTPUT} {KR_CGS_OUTPUT} {KR_RENDERS_OUTPUT} {KR_FRAMELESS_OUTPUT} {GLOBAL_FRAMELESS_OUTPUT} {GLOBAL_RENDERS_OUTPUT} {GLOBAL_CGS_OUTPUT}"
    )
    os.system(f"rm {CHARAS_OUTPUT}")
    os.system("rm -r assets")
