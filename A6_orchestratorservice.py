from A1_audio_loader import load_audio
from A2_privacy_killswitch import privacy_switch
from A2_x_privacy_move import movefiles
from A3_classify import classify
from A4_embeddinglayer import device, embed
from db_service_audio import sendaudiotodb

def main():
    audioload = load_audio()
    killswitch = privacy_switch(audioload)
    safe_files, speechfiles  = killswitch
    movefiles(speechfiles)
    classification = classify(safe_files)
    dev = device()
    fembedding = embed(dev, classification)
    sendaudiotodb(fembedding)


if __name__ == "__main__":
    main()
