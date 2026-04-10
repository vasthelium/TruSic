from app.services.A1_audio_loader import load_audio
from app.services.A2_privacy_killswitch import privacy_switch
from app.services.A2_x_privacy_move import movefiles
from app.services.A3_classify import classify
from app.ml.embeddings.A4_embeddinglayer import device, embed
from app.db.db_service_audio import sendaudiotodb

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
