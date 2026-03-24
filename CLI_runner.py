from db_service_human import upsrt_oura, sendstatetriggersdb
from A5_kNN_Trusic import trusic_NN
import argparse
from H5_trigger_states import build_statetriggers

def main(args):
    if args.mode == "oura":
        upsrt_oura()
    elif args.mode == "statetriggers":
        statetriggers = build_statetriggers()
        sendstatetriggersdb(statetriggers)
    elif args.mode == "retrieval":
        trusic_NN()

if __name__ == "__main__":
    parser = argparse.ArgumentParser() #tool that knows how to read CLI input
    parser.add_argument("--mode", required=True) # Expect a value called --mode from the user

    args = parser.parse_args() #Take the raw CLI input and convert it into a structured object (args)
    main(args) 
    


