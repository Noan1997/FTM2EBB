import pandas as pd
import os
import pdb

def ClearScreen():
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")

def FindSongName(ftm, column, search_song_name, ROWSong):
    for index, row in ftm.iterrows():
        if pd.notna(row[column]) and search_song_name.lower() in str(row[column]).lower():
            return search_song_name
    
    print(f"The song '{search_song_name}' was not found in the FTM file.")
    return None

def FindRowSong(ftm, column, search_song_name, ROWSong):
    for index, row in ftm.iterrows():
        if pd.notna(row[column]) and search_song_name.lower() in str(row[column]).lower():
            ROWSong = index # Saves the row where the song is located
            return ROWSong
            
def FindRowDataSong(ftm, column, search_song_name, ROWSong, ROWData):
    for index in range(ROWSong, len(ftm)):
        row = ftm.iloc[index]
        if pd.notna(row[column]) and search_song_name.lower() in str(row[column]).lower():
            ROWData = index  # Guarda la fila donde se encuentra la canción
            return ROWData + 1

def MakeHeaderSong(SN, Tempo, TN, NC):
    SN_NameFile = SN.replace(" ", "_")
    with open(f"{SN_NameFile}_Header.asm", 'w') as Header_file:
        Header_file.write("\t;Paste header along with the other songs headers\n")
        Header_file.write(f"\t.db $00, ${Tempo}\n")
        if NC >= 1:
            Header_file.write(f"\t.dw SQ1_TRACK_0x{TN}_PTRS, ")
        else:
            Header_file.write("\t.dw $FFFF, ")
        if NC >= 2:
            Header_file.write(f"SQ2_TRACK_0x{TN}_PTRS\n")
        else:
            Header_file.write("$FFFF\n")
        if NC >= 3:
            Header_file.write(f"\t.dw TRI_TRACK_0x{TN}_PTRS, ")
        else:
            Header_file.write("\t.dw $FFFF, ")
        if NC >= 4:
            Header_file.write(f"NSE_TRACK_0x{TN}_PTRS")
        else:
            Header_file.write("$FFFF")
            
def ReadSongBlocks(ftm, ROWSong, SQ1Blocks, SQ2Blocks, TRIBlocks, NSEBlocks):
    ROWSongBlocks = ROWSong + 4
    while ROWSongBlocks < len(ftm):
        BlocksData = ftm.loc[ROWSongBlocks, 'SQ1_Channel']
        if pd.isna(BlocksData) or BlocksData.strip() == "":
            break
        Blocks = BlocksData.split()
        
        if len(Blocks) >= 4:
            SQ1Blocks.append(Blocks[0])
            SQ2Blocks.append(Blocks[1])
            TRIBlocks.append(Blocks[2])
            NSEBlocks.append(Blocks[3])
            
        ROWSongBlocks += 1
    return SQ1Blocks, SQ2Blocks, TRIBlocks, NSEBlocks

def WriteSongBlocks(FILE, TN, NC, LP, CLP, LPPC, BP, CN, CnlBlocks):
    Channel_Block_Count = 0
    for Blocks in range(len(CnlBlocks)):
        if (LP == 2 and NC > 0 and NC <= CLP and Channel_Block_Count == LPPC[NC-1]):
            FILE.write(f"{CN[NC]}_TRACK_0x{TN}_LOOP:\n")
        elif (LP == 1 and Channel_Block_Count == BP):
            FILE.write(f"{CN[NC]}_TRACK_0x{TN}_LOOP:\n")
        FILE.write(f"\t.dw {CN[NC]}_TRACK_0x{TN}_BLOCK_{CnlBlocks[Blocks]}\n")
        Channel_Block_Count += 1
    if(LP == 3):
        FILE.write("\t.dw $0000\n")
    elif(LP == 2 and NC > 0 and NC <= CLP or LP == 1):
        FILE.write("\t.dw $FFFF\n")
        FILE.write(f"\t.dw {CN[NC]}_TRACK_0x{TN}_LOOP\n")
    else:
        FILE.write("\t.dw $FFFF\n")
        FILE.write(f"\t.dw {CN[NC]}_TRACK_0x{TN}_PTRS\n")
        
def SetTrimbreConfig(Bank, NTC, NTB, CN, TimbreBlocks,  SQ1Timbres, SQ2Timbres, TRITimbres):
    #SQ1 and SQ2 timbre data
    PitchEnvelope = None
    VolumeEnvelope = None
    DecimalVolumeEnvelope = None
    DutyTimbre = None
#   VolumeSetup = None
    VolumeTimbre = None
    DecimalVolumeTimbre = None
    #TRI timbre data
    AutoReleaseSetup = None
    BeforeAutoRelease = None
    TimeAutoRelease = None
    for J in range(NTB):
        ClearScreen()
        if NTC == 2:
            while True:
                try:
                    print(f"Activate auto-release in block {TimbreBlocks[NTC][J]} of channel {CN[NTC+1]}?\n")
                    print("\t 0-7 or 6-7- Activated")
                    print("\t 2-5- Disabled")
                    print("\t NOTE: If you don't know how to use it, it's recommended to leave it at 2-5 (Disabled)")
                    AutoReleaseSetup = int(input())
                    if (AutoReleaseSetup >= 0 and AutoReleaseSetup <= 7):
                        ClearScreen()
                        break
                    else:
                        print("Error: Please select a valid option.")
                except:
                    print("Invalid entry. Please select a valid option.")
            if (AutoReleaseSetup >= 2 and AutoReleaseSetup <=5):
                BeforeAutoRelease = 00
                TimeAutoRelease = 00
            else:
                while True:
                    try:
                        print('"Set the number of quarter-frames to play notes before auto-release." (TRI Channel) -Quantam\n')
                        print("Values: 00-7F")
                        print("\t NOTE: It's recommended to leave it at 0")
                        BeforeAutoRelease = input().strip()
                        BeforeAutoRelease = int(BeforeAutoRelease, 16)
                        if (BeforeAutoRelease >= 0 and BeforeAutoRelease <= 127):
                            ClearScreen()
                            break
                        else:
                            print("Error: Please select a valid option.")
                    except:
                        print("Invalid entry. Please select a valid option.")
                    
                    while True:
                        try:
                            print('"Set auto-release time to x quarter-frames." (TRI Channel) -Quantam\n')
                            print("Values: 00-1F")
                            print("\t NOTE: It's recommended to leave it at 0")
                            TimeAutoRelease = input().strip()
                            TimeAutoRelease = int(TimeAutoRelease, 16)
                            if (TimeAutoRelease >= 0 and TimeAutoRelease <= 31):
                                ClearScreen()
                                break
                            else:
                                print("Error: Please select a valid option.")
                        except:
                            print("Invalid entry. Please select a valid option.")
            BinAutoReleaseSetup = bin(AutoReleaseSetup)[2:].zfill(3)
            BinTimeAutoRelease = bin(TimeAutoRelease)[2:].zfill(5)
            BinBeforeAutoRelease = bin(BeforeAutoRelease)[2:].zfill(7)
            TRITimbres.append(f"%{BinAutoReleaseSetup}{BinTimeAutoRelease},%0{BinBeforeAutoRelease}")

        else:
            while True:
                try:
                    print(f"What tone envelope do you need in block {TimbreBlocks[NTC][J]} of channel {CN[NTC+1]}?\n")
                    print("\t 1 or 7-Envelope 1 and 7 @8a33: | +0 +1 +1 +2 +1 +0 -1 -1 -2 -1")
                    print("\t 5-Envelope 5 @8a12: +0 +0 +0 +0 +0 +0 +0 +0 +0 +0 +0 +0 +0 +0 +0 +1 +0 +0 +0 +0 -1 +0 +0 +0 +0 +1 +1 +0 +0 +0 -1 -1 +0 | +0 +1 +1 +2 +1 +0 -1 -1 -2 -1")
                    print("\t 2-Envelope 2 @8a3d: +0 -1 -2 -3 -4 -5 -6 -7 -8 -9 -10 -11 -10 -9 -10 -11 | -10")
                    print('\t 3-Envelope 3 ("Is hard-coded to -2 period units. Oddly, it checks whether the key number is < $4c/2 = $26, but then sets the offset to -2 in both cases." -Quantam)')
                    print("\t 4 or 6-Envelope 4 and 6 @8a06: +9 +8 +7 +6 +5 +4 +3 +2 +2 +1 +1 +0 +0 +0 +0 +0 +0 +0 +0 +0 +0 +0 +0 +0 +0 +0 +0 +1 +0 +0 +0 +0 -1 +0 +0 +0 +0 +1 +1 | +0 +0 +0 -1 -1 +0 +0 +1 +1 +2")
                    print('WARNING:"Envelopes 4 and 6 are simple (identical) vibrato envelopes, but hard-coded to NOT apply to key $46/2 = $23" -Quantam')
                    PitchEnvelope = int(input())
                    if (PitchEnvelope >= 1 and PitchEnvelope <= 7):
                        ClearScreen()
                        break
                    else:
                        print("Error: Please select a valid option.")
                except:
                    print("Invalid entry. Please select a valid option.")

            while True:
                try:
                    print("Select the duty to use in the timbre settings\n")
                    print("\t 0-00 (12.5%)")
                    print("\t 1-01 (25%)")
                    print("\t 2-10 (50%)")
                    print("\t 3-11 (75%)")
                    DutyTimbre = int(input())
                    if (DutyTimbre >= 0 and DutyTimbre <= 3):
                        ClearScreen()
                        break
                    else:
                        print("Error: Please select a valid option.")
                except:
                    print("Invalid entry. Please select a valid option.")
                       
            while True:
                try:
                    print("Select the base volume to use in the timbre settings\n")
                    print("Values: 00-0F")
                    VolumeTimbre = input().strip()
                    DecimalVolumeTimbre = int(VolumeTimbre, 16)
                    if (DecimalVolumeTimbre >= 0 and DecimalVolumeTimbre <= 15):
                        ClearScreen()
                        break
                    else:
                        print("Error: Please select a valid option.")
                except:
                    print("Invalid entry. Please select a valid option.")
                           
            while True:
                try:
                    print(f"Set the volume envelope used for block {TimbreBlocks[NTC][J]} of channel {CN[NTC+1]}?\n")
                    if Bank == 1:
                        print("\t Envelope  1 @874c: 233456776554 ff")
                        print("\t Envelope  2 @8753: 5a9888776666655555 ff")
                        print("\t Envelope  3 @8777: 111122223333444444455555556666777888 ff")
                        print("\t Envelope  4 @878a: f987777766655544 ff")
                        print("\t Envelope  5 @879c: a876 ff")
                        print("\t Envelope  6 @87a2: 99 ff")
                        print("\t Envelope  7 @8745: 235678888887 ff")
                        print("\t Envelope  8 @87a4: dcba998887765544 ff")
                        print("\t Envelope  9 @87ad: 2344333333333332 ff")
                        print("\t Envelope  a @879f: 7432 ff")
                        print("\t Envelope  b @87b6: 777665554443322211111111 f0")
                        print("\t Envelope  c @87c3: 54433333322222111111111111 f0")
                        print("\t Envelope  d @87d1: 433322222221111111111111 f0")
                        print("\t Envelope  e @87de: 3222222111111111111111 f0")
                        print("\t Envelope  f @87ea: 211111111111111111 f0")
                        print("\t Envelope 10 @87f4: 998877766655544433333332222222222111111111111111 f0")
                        print("\t Envelope 11 @883f: 23455544333322 ff")
                        print("\t Envelope 12 @8847: 87654321443321113221111121111111111111 ff")
                        print("\t Envelope 13 @880d: 6555544433333333222222221111111111111111 f0")
                        print("\t Envelope 14 @885b: 666542213221111121111111111111 ff")
                        print("\t Envelope 15 @8822: fbbaaa99999998887777776666665554444443333322222222111111 f0")
                        print("\t Envelope 16 @8718: 7611111431 ff")
                        print("\t Envelope 17 @875d: 111122223333444444455555556666777888765432 ff")
                        print("\t Envelope 18 @873c: 9876632287765311 f0")
                        print("\t Envelope 19 @8735: 233332222222 ff")
                        print("\t Envelope 1a @8722: 433322222222222111111111111111111111 f0")
                        print("\t Envelope 1b @871e: 334566 ff")
                        print("\t Envelope 1c @8773: 111122 ff")
                        print("\t Envelope 1d @8793: c876666655555544 ff")
                        print("\t Envelope 1e @886b: a8754321433321113221111121111111111111 ff")
                    else:
                        print("\t Envelope  1 @8ee9: 233456776554 ff")
                        print("\t Envelope  2 @8ef0: 5a9888776666655555 ff")
                        print("\t Envelope  3 @8f14: 111122223333444444455555556666777888 ff")
                        print("\t Envelope  4 @8f27: f987777766655544 ff")
                        print("\t Envelope  5 @8f30: a876 ff")
                        print("\t Envelope  6 @8f36: 99 ff")
                        print("\t Envelope  7 @8ee2: 235678888887 ff")
                        print("\t Envelope  8 @8f38: dcba998887765544 ff")
                        print("\t Envelope  9 @8f41: 2344333333333332 ff")
                        print("\t Envelope  a @8f33: 7432 ff")
                        print("\t Envelope  b @8f4a: 7776655544433221 f0")
                        print("\t Envelope  c @8f53: 44433332221111 f0")
                        print("\t Envelope  d @8f5b: 33332222111111 f0")
                        print("\t Envelope  e @8f63: 222222111111 f0")
                        print("\t Envelope  f @8f6a: 1111111111110100 f0")
                        print("\t Envelope 10 @8f73: 998877766655544433333332222222222111111111111111 f0")
                        print("\t Envelope 11 @8fbe: 23455544333322 ff")
                        print("\t Envelope 12 @8fc6: 87654321443321113221111121111111111111 ff")
                        print("\t Envelope 13 @8f8c: 6555544433333333222222221111111111111111 f0")
                        print("\t Envelope 14 @8fda: 666542213221111121111111111111 ff")
                        print("\t Envelope 15 @8fa1: fbbaaa99999998887777776666665554444443333322222222111111 f0")
                        print("\t Envelope 16 @8ebd: 7611111431 ff")
                        print("\t Envelope 17 @8efa: 111122223333444444455555556666777888765432 ff")
                        print("\t Envelope 18 @8ed9: 9876632287765311 f0")
                        print("\t Envelope 19 @8ed2: 233332222222 ff")
                        print("\t Envelope 1a @8ec7: 91919191919191919191 f0")
                        print("\t Envelope 1b @8ec3: 334566 ff")
                        print("\t Envelope 1c @8f10: 111122 ff")
                    VolumeEnvelope = input().strip()
                    DecimalVolumeEnvelope = int(VolumeEnvelope, 16)
                    if (DecimalVolumeEnvelope >= 1 and DecimalVolumeEnvelope <= 28 or DecimalVolumeEnvelope >= 1 and DecimalVolumeEnvelope <= 30):
                        ClearScreen()
                        break
                    else:
                        print("Error: Please select a valid option.")
                except:
                    print("Invalid entry. Please select a valid option.")
            BinPitchEnvelope = bin(PitchEnvelope)[2:].zfill(3)
            BinVolumeEnvelope = bin(DecimalVolumeEnvelope)[2:].zfill(5)
            BinDutyTimbre = bin(DutyTimbre)[2:].zfill(2)
            BinVolumeTimbre = bin(DecimalVolumeTimbre)[2:].zfill(4)
            if NTC == 0:
                SQ1Timbres.append(f"%{BinPitchEnvelope}{BinVolumeEnvelope},%{BinDutyTimbre}11{BinVolumeTimbre}")
            if NTC == 1:
                SQ2Timbres.append(f"%{BinPitchEnvelope}{BinVolumeEnvelope},%{BinDutyTimbre}11{BinVolumeTimbre}")
                
def ReadData(ftm, start_row, max_blocks, Tempo, noise_dict, dmc_dict, data):
    # Always work with 5 channels
    num_channels = 5
    
    # Ensure max_blocks has 5 elements
    if len(max_blocks) < num_channels:
        max_blocks = list(max_blocks) + [0] * (num_channels - len(max_blocks))
    
    # Initialize data with 5 sublists
    if not data:
        data = [[] for _ in range(num_channels)]
    elif len(data) < num_channels:
        data.extend([[] for _ in range(num_channels - len(data))])
    
    # Column configuration
    CHANNEL_COLS = [
        "SQ1_Channel",
        "SQ2_Channel",
        "TRI_Channel",
        "NSE_Channel",
        "DMC_Channel"
    ]
    
    # Function to convert duration to hexadecimal
    def convert_duration(duration_frames, tempo_list):
        if duration_frames in tempo_list:
            return hex(tempo_list.index(duration_frames))[2:]
        else:
            return f"{hex(int(duration_frames))[2:]}?"
    
    # Function to process NSE with special cases
    def process_nse_value(nse_str):
        if not nse_str or nse_str.strip() in ['---', '...', '..', '.', '']:
            return 0
        
        # Split the string and remove irrelevant parts
        parts = [p for p in nse_str.strip().split() if p not in ['...', '..', '.', '']]
        if not parts:
            return 0
        
        first_part = parts[0]
        if first_part == 'E-#':
            if len(parts) >= 2:
                try:
                    hex_value = int(parts[1], 16)
                    return 4 if hex_value > 0 else 0
                except ValueError:
                    return 0
            return 0
        elif len(parts) >= 2:
            key = ' '.join(parts[:2])  # e.g., "C-# 0B"
            return noise_dict.get(key, 0)
        return noise_dict.get(first_part, 0)

    # Process melodic channels (SQ1, SQ2, TRI)
    for chan_idx in range(3):
        if max_blocks[chan_idx] <= 0:
            continue
            
        col_name = CHANNEL_COLS[chan_idx]
        if col_name not in ftm.columns:
            continue
            
        channel_blocks = []
        current_block = []
        current_note = None
        note_duration = 0
        none_count = 0
        is_first_block = True
        last_note_info = None
        last_was_none = False
        
        for idx in range(start_row, len(ftm)):
            if none_count >= 2:
                break
                
            raw_val = ftm.at[idx, col_name]
            
            if pd.isnull(raw_val):
                none_count += 1
                last_was_none = True  # Mark that the last event was None
                
                if none_count == 1:
                    # Save current note only if it has duration > 0
                    if current_note is not None and note_duration > 0:
                        frames = note_duration * Tempo[0]
                        hex_dur = convert_duration(frames, Tempo)
                        current_block.append([current_note, hex_dur])
                        
                        if current_block:
                            last_block_idx = len(channel_blocks)
                            last_note_idx = len(current_block) - 1
                            last_note_info = (last_block_idx, last_note_idx, note_duration)
                    
                    # Save block only if it has notes
                    if current_block:
                        channel_blocks.append(current_block)
                        if len(channel_blocks) >= max_blocks[chan_idx]:
                            break
                    
                    # Prepare new block
                    current_block = []
                    current_note = None
                    note_duration = 0
                    is_first_block = False
                continue
                
            none_count = 0
            last_was_none = False  # Reset if not None
            val = str(raw_val).strip()
            note_part = val[:4].strip()
            
            ValidNote = False
            
            # Process only if it's a valid value
            if not note_part or note_part in ['...', '..', '.', '']:
                # If there's a current note, extend its duration
                if current_note is not None:
                    note_duration += 1
                # First "..." as rest only in first block
                elif is_first_block:
                    ValidNote = True
                    current_note = 'rest'
                    note_duration = 1
                continue
            
            # Process valid note
            if note_part == '---':
                ValidNote = True
                processed_note = 'rest'
            elif len(note_part) >= 3 and note_part[0] in 'ABCDEFG':
                ValidNote = True
                note_char = note_part[0]
                accidental = 's' if len(note_part) > 1 and note_part[1] == '#' else ''
                octave = note_part[2] if len(note_part) > 2 and note_part[2].isdigit() else '3'
                try:
                    octave = str(int(octave) + 1)
                except:
                    octave = '4'
                processed_note = f"{note_char}{accidental}{octave}"
            else:
                # Unrecognized value - ignore
                continue
            
            # Handle note change
            if ValidNote == True:
                # Save previous note only if it has duration > 0
                if current_note is not None and note_duration > 0:
                    frames = note_duration * Tempo[0]
                    hex_dur = convert_duration(frames, Tempo)
                    current_block.append([current_note, hex_dur])
                    
                    if current_block:
                        last_block_idx = len(channel_blocks)
                        last_note_idx = len(current_block) - 1
                        last_note_info = (last_block_idx, last_note_idx, note_duration)
                
                # Start new note
                current_note = processed_note
                note_duration = 1
            else:
                # Same note - extend duration
                note_duration += 1
        
        # Save last note if it has duration > 0 and didn't end with None
        if current_note is not None and note_duration > 0 and not last_was_none:
            frames = note_duration * Tempo[0]
            hex_dur = convert_duration(frames, Tempo)
            current_block.append([current_note, hex_dur])
            
            if current_block:
                last_block_idx = len(channel_blocks)
                last_note_idx = len(current_block) - 1
                last_note_info = (last_block_idx, last_note_idx, note_duration)
        
        # Save last block if it has notes
        if current_block:
            channel_blocks.append(current_block)
        
        data[chan_idx] = channel_blocks[:max_blocks[chan_idx]]
    
    # Process NSE and DMC together
    nse_enabled = max_blocks[3] > 0
    dmc_enabled = max_blocks[4] > 0
    if nse_enabled or dmc_enabled:
        channel_blocks = []
        current_block = []
        current_note = None
        note_duration = 0
        none_count = 0
        last_note_info = None

        for idx in range(start_row, len(ftm)):
            if none_count >= 2:
                break
            nse_val = ftm.at[idx, "NSE_Channel"] if "NSE_Channel" in ftm.columns else None
            dmc_val = ftm.at[idx, "DMC_Channel"] if "DMC_Channel" in ftm.columns else None
            if pd.isnull(nse_val) and pd.isnull(dmc_val):
                none_count += 1
                if none_count == 1:
                    # Save current note only if it has duration > 0
                    if current_note is not None and note_duration > 0:
                        frames = note_duration * Tempo[0]
                        hex_dur = convert_duration(frames, Tempo)
                        current_block.append([current_note, hex_dur])
                        
                        if current_block:
                            last_block_idx = len(channel_blocks)
                            last_note_idx = len(current_block) - 1
                            last_note_info = (last_block_idx, last_note_idx, note_duration)
                    
                    # Save block only if it has notes
                    if current_block:
                        channel_blocks.append(current_block)
                        if len(channel_blocks) >= max_blocks[chan_idx]:
                            break
                    
                    # Prepare new block
                    current_block = []
                    current_note = None
                    note_duration = 0
                continue
            
            none_count = 0
            nse_str = str(nse_val).strip() if not pd.isnull(nse_val) else ""
            dmc_str = str(dmc_val).strip() if not pd.isnull(dmc_val) else ""

            # Ignore rows where both columns are holds
            if nse_str in ['...', '..', '.', ''] and dmc_str in ['...', '..', '.', '']:
                if current_note is not None:
                    note_duration += 1
                continue

            # Process valid notes
            nsevalidval = False
            dmcvalidval = False
            generalval = False
            if nse_str not in ['...', '..', '.', ''] or dmc_str not in ['...', '..', '.', '']:
                nse_value=1
                dmc_value=0
                if(len(nse_str)>=3 and nse_str[0] in '0123456789ABCDEFG'):
                    nse_value = process_nse_value(nse_str) if nse_enabled and nse_str not in ['...', '..', '.', ''] else 0
                    nsevalidval = True
                if(len(dmc_str)>=3 and dmc_str[0] in 'ABCDEFG'):
                    dmc_key = dmc_str[:4].strip() if dmc_str not in ['...', '..', '.', ''] else ""
                    dmc_value = dmc_dict.get(dmc_key, 0) if dmc_key else 0
                    dmcvalidval = True           
                if(nsevalidval==True or dmcvalidval==True):
                    combined_byte = (dmc_value << 6) | nse_value
                    processed_note = f"{combined_byte:02X}"
                    generalval = True

            if current_note is None:
                current_note = processed_note
                note_duration = 1
            elif current_note == processed_note and generalval == False:
                note_duration += 1
            else:
                frames = note_duration * Tempo[0]
                hex_dur = convert_duration(frames, Tempo)
                current_block.append([current_note, hex_dur])
                current_note = processed_note
                note_duration = 1

        # Add the last note
        if current_note is not None and note_duration > 0:
            frames = note_duration * Tempo[0]
            hex_dur = convert_duration(frames, Tempo)
            current_block.append([current_note, hex_dur])
        if current_block:
            channel_blocks.append(current_block)

        if nse_enabled:
            data[3] = channel_blocks[:max_blocks[3]]
        if dmc_enabled:
            data[4] = channel_blocks[:max_blocks[4]]
    if(num_channels==5):
        data.pop()
        max_blocks.pop()
    return data

def WriteData(output_file, TN, TR, TBlocks, SQ1T, SQ2T, TRIT, NC, CBN, NotesChannels):
    # Writing data to the output file
    output_file.write(f"\t.include \"Note_table_EBB.i\"\n")
    for channel in range(len(NotesChannels)):
        for block_index in range(len(NotesChannels[channel])):
            previous_length = 0  # Reset for each block
            Current_Channel = NotesChannels[channel]
            if len(Current_Channel[block_index]) > 0:
                output_file.write(f"{NC[channel+1]}_TRACK_0x{TN}_BLOCK_{CBN[channel][block_index]}:")
                # Check if timbre data should be written
                if(channel>=0 and channel<=2):
                    if block_index in TBlocks[channel]:  # Adjust this logic if necessary
                        if channel == 0 and block_index < len(SQ1T):
                            output_file.write(f"\n\t.db $9F,{SQ1T[block_index]}")
                        elif channel == 1 and block_index < len(SQ2T):
                            output_file.write(f"\n\t.db $9F,{SQ2T[block_index]}")
                        elif channel == 2 and block_index < len(TRIT):
                            output_file.write(f"\n\t.db $9F,{TRIT[block_index]}")
                # Write notes
                for note, note_length in Current_Channel[block_index]:
                    if note_length == previous_length and channel == 3:
                        output_file.write(f",${note}")
                    elif note_length == previous_length:
                        output_file.write(f",{note}")
                    elif note_length != previous_length and channel == 3:
                        output_file.write(f"\n\t.db $B{note_length},${note}")
                        previous_length = note_length
                    else:
                        output_file.write(f"\n\t.db $B{note_length},{note}")
                        previous_length = note_length
                output_file.write("\n\t.db $00\n")
            else:
                print(f"Warning: No data in NotesChannels for channel {channel}, block {block_index}.")
        if(block_index+1<len(CBN[channel])):
            valueloop = hex((3 << 6) | int(int(TR) / 2)) #Set Loop value
            valloop = valueloop.upper()
            output_file.write(f"{NC[channel+1]}_TRACK_0x{TN}_BLOCK_{CBN[channel][len(CBN[channel])-1]}:")  #Start Extra Block
            output_file.write(f"\n\t.db ${valloop[2:]}") #Start Loop
            output_file.write(f"\n\t.db $B1,rest")
            output_file.write(f"\n\t.db $FF") #End Loop
            output_file.write(f"\n\t.db $00\n") #End Extra Block
