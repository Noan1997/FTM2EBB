""" FTM2EBB script """

import sys
import pandas as pd
from subroutinesF2M import *

Tempos = (
#Tempo0x1C 
    (
    [4, 8, 16, 32, 64, 24, 48, 12, 10, 5, 2, 1],   #0 = T_0x0_225
    [5, 10, 20, 40, 80, 30, 60, 15, 12, 6, 3, 2],   #1 = T_0xC_180
    [6, 12, 24, 48, 96, 36, 72, 18, 16, 8, 3, 1, 4, 2, 0, 144], #2 = T_0x18_150
    [7, 14, 28, 56, 112, 42, 84, 21, 18, 9, 3, 1, 2],   #3 = T_0x28_129
    [8, 16, 32, 64, 128, 48, 96, 24, 21, 10, 4, 1, 2, 192], #4 = T_0x35_113
    [9, 18, 36, 72, 144, 54, 108, 27, 24],  #5 = T_0x43_100
    [10, 20, 40, 80, 160, 60, 120, 30, 26, 13, 5, 1, 2, 23],    #6 = T_0x4C_90
    [11, 22, 44, 88, 176, 66, 132, 33, 29, 14, 5, 1, 2, 23] #7 = T_0x5A_82
    ),
#Tempo0x1B
    (
    [4, 8, 16, 32, 64, 24, 48, 12, 10, 5, 2, 1],   #0 = T_0x0_225
    [5, 10, 20, 40, 80, 30, 60, 15, 12, 6, 3, 2],   #1 = T_0xC_180
    [6, 12, 24, 48, 96, 36, 72, 18, 16, 8, 3, 1, 4, 2, 0, 144], #2 = T_0x18_150
    [7, 14, 28, 56, 112, 42, 84, 21, 18, 9, 3, 1, 2],   #3 = T_0x28_129
    [7, 15, 30, 60, 120, 45, 90, 22, 20, 10, 3, 1, 8], #4 = T_0x35_120
    [8, 16, 32, 64, 128, 48, 96, 24, 21, 10, 4, 1, 2, 192], #5 = T_0x42_113
    [9, 18, 36, 72, 144, 54, 108, 27, 24],  #6 = T_0x50_100
    [10, 20, 40, 80, 160, 60, 120, 30, 26, 13, 5, 1, 2, 23],    #7 = T_0x59_90
    [11, 22, 44, 88, 176, 66, 132, 33, 29, 14, 5, 1, 2, 23] #8 = T_0x67_82
    ),
    {0:'00',1:'0C',2:'18',3:'28',4:'35',5:'43',6:'4C',7:'5A'},
    {0:'00',1:'0C',2:'18',3:'28',4:'35',5:'42',6:'50',7:'59',8:'67'}
    )
ChannelsNames = {1:'SQ1',2:'SQ2',3:'TRI',4:'NSE',5:'DMC'}
NSE_dict = {'7-# 0C':2,'C-# 0B':7,'9-#':10,'C-# 0C':13,'B-#':16,'A-#':19,'5-#':22,'7-# 03':25,'1-#':28}
DMC_dict = {'C-3':1,'D-3':2}
ROWSong = None
start_row = None
DevMode=0
if __name__ == '__main__':
    if(DevMode!=1):
        print("Enter the name of the FTM file (TXT format)")
    
    ftmname = input().strip().replace("'", "").replace('"', "")
    
    if not ftmname.lower().endswith('.txt'):
        print("Error: The file must have the extension .txt")
    else:
        try:
            with open(ftmname, 'r') as file:
                lines = file.readlines()

                data = [line.strip().split(':') for line in lines]

                ftm = pd.DataFrame(data, columns=['ROW_Number', 'SQ1_Channel', 'SQ2_Channel',
                            'TRI_Channel', 'NSE_Channel', 'DMC_Channel'])

            # Find the song name in the 'ROW_Number' column
            ClearScreen()
            if(DevMode!=1):
                print("Enter the name of the song:")
            Search_Song_name = input().strip()
            Song_name = FindSongName(ftm, 'ROW_Number', Search_Song_name, ROWSong)
            if Song_name is not None:
                ClearScreen()
                print(Song_name)

            ROWSong = FindRowSong(ftm, 'ROW_Number', Search_Song_name, ROWSong)
            Song_name_FILE = Song_name.replace(" ", "_")

            if(DevMode!=1):
                print("Enter the track's ID number (In EBB/Mother Game)")
            Number_Track = input()
            if(DevMode!=1):
                print("Enter the track's number rows (Famitracker rows per pattern)")
            Number_Rows = int(input())
            if(DevMode!=1):
                print("Enter the number of channels used in the track")
            Number_Channels = int(input())
            Bank_Track = None
            while True:
                try:
                    if(DevMode!=1):
                        print("Select the bank where the track will be located\n \t 0-Bank0x1C\n \t 1-Bank0x1B")
                    Bank_Track = int(input())
                    if(Bank_Track >= 0 and Bank_Track <=1):
                        break
                    else:
                        print("Error: Please select a valid option.")
                except ValueError:
                        print("Invalid entry. Please select a valid option.")

            ClearScreen()
            Tempo_Track = None
            while True:
                try:
                    if(DevMode!=1):
                        print("Select the tempo used for the track (EBB/Mother Format):\n")
                    if Bank_Track == 1:
                        #Tempos Bank0x1B
                        if(DevMode!=1):
                            print("\t 0-225 BPM (0x00)")
                            print("\t 1-180 BPM (0x0C)")
                            print("\t 2-150 BPM (0x18)")
                            print("\t 3-129 BPM (0x28)")
                            print("\t 4-120 BPM (0x35)")
                            print("\t 5-113 BPM (0x42)")
                            print("\t 6-100 BPM (0x50)")
                            print("\t 7-90 BPM (0x59)")
                            print("\t 8-82 BPM (0x67)")
                        Tempo_Track = int(input())
                        if(Tempo_Track >= 0 and Tempo_Track <=8):
                            break
                        else:
                            print("Error: Please select a valid option.")
                            ClearScreen()
                        #Tempos Bank0x1B
                    else:
                        if(DevMode!=1):
                            print("\t 0-225 BPM (0x00)")
                            print("\t 1-180 BPM (0x0C)")
                            print("\t 2-150 BPM (0x18)")
                            print("\t 3-129 BPM (0x28)")
                            print("\t 4-113 BPM (0x35)")
                            print("\t 5-100 BPM (0x43)")
                            print("\t 6-90 BPM (0x4C)")
                            print("\t 7-82 BPM (0x5A)")
                        Tempo_Track = int(input())
                        if(Tempo_Track >= 0 and Tempo_Track <=7):
                            break
                        else:
                            print("Error: Please select a valid option.")
                            ClearScreen()
                except ValueError:
                        print("Invalid entry. Please select a valid option.")
                        ClearScreen()
            #Create song header
            print("Creating header file...")
            MakeHeaderSong(Song_name, Tempos[Bank_Track+2][Tempo_Track], Number_Track, Number_Channels)
            SQ1Blocks = []
            SQ2Blocks = []
            TRIBlocks = []
            NSEBlocks = []
            #Create playlist of the song
            print("Creating Block Playlist file...")
            ReadSongBlocks(ftm, ROWSong, SQ1Blocks, SQ2Blocks, TRIBlocks, NSEBlocks)
            SQ1BlocksData = list(dict.fromkeys(SQ1Blocks))
            SQ2BlocksData = list(dict.fromkeys(SQ2Blocks))
            TRIBlocksData = list(dict.fromkeys(TRIBlocks))
            NSEBlocksData = list(dict.fromkeys(NSEBlocks))          
            LoopPoint = None
            BlockPoint = None
            ChnlsLoopPoint = None
            LoopPointPerCnl = []

            while True:
                try:
                    if(DevMode!=1):
                        print("Do you want to set loop point?")
                        print("\t 0-Basic Global Loop")
                        print("\t 1-Global Loop Point")
                        print("\t 2-Block Point for each channel")
                        print("\t 3-No loop points")
                    LoopPoint = int(input())
                    if (LoopPoint == 1):
                        if(DevMode!=1):
                            print("Write the ORDER number where the global loop occurs.")
                        BlockPoint = int(input())
                    elif (LoopPoint == 2):
                        if(DevMode!=1):
                            print("Enter the number of channels with loop points")
                        ChnlsLoopPoint = int(input())
                        for i in range(ChnlsLoopPoint):
                            if(DevMode!=1):
                                print(f"Write the ORDER number where the global loop occurs in {ChannelsNames[i+1]}.")
                            BlockPoint = int(input())
                            LoopPointPerCnl.append(BlockPoint)
                    if (LoopPoint >=0 and LoopPoint <=3):
                        break
                    else:
                        print("Error: Please select a valid option.")
                except ValueError:
                        print("Invalid entry. Please select a valid option.")
            
            with open(f"{Song_name_FILE}_Playlist.asm", 'w') as PlaylistFile:
                if Number_Channels >= 1:
                    Number_Channel = 1
                    PlaylistFile.write(f"SQ1_TRACK_0x{Number_Track}_PTRS:\n")
                    WriteSongBlocks(PlaylistFile, Number_Track, Number_Channel, LoopPoint, ChnlsLoopPoint, LoopPointPerCnl, BlockPoint, ChannelsNames, SQ1Blocks)
                if Number_Channels >= 2:
                    Number_Channel = 2
                    PlaylistFile.write(f"SQ2_TRACK_0x{Number_Track}_PTRS:\n")
                    WriteSongBlocks(PlaylistFile, Number_Track, Number_Channel, LoopPoint, ChnlsLoopPoint, LoopPointPerCnl, BlockPoint, ChannelsNames, SQ2Blocks)
                if Number_Channels >= 3:
                    Number_Channel = 3
                    PlaylistFile.write(f"TRI_TRACK_0x{Number_Track}_PTRS:\n")
                    WriteSongBlocks(PlaylistFile, Number_Track, Number_Channel, LoopPoint, ChnlsLoopPoint, LoopPointPerCnl, BlockPoint, ChannelsNames, TRIBlocks)
                if Number_Channels >= 4:
                    Number_Channel = 4
                    PlaylistFile.write(f"NSE_TRACK_0x{Number_Track}_PTRS:\n")
                    WriteSongBlocks(PlaylistFile, Number_Track, Number_Channel, LoopPoint, ChnlsLoopPoint, LoopPointPerCnl, BlockPoint, ChannelsNames, NSEBlocks)
            # Set timbre configuration for SQ1, SQ2 and TRI channels
            SQ1Timbres = []
            SQ2Timbres = []
            TRITimbres = []
            TimbreBlocks = [[],[],[]]
            Trimbreconfig = None
            ClearScreen()
            while True:
                try:
                    if(DevMode!=1):
                        print("Set the timbre settings for channels SQ1, SQ2, and TRI.\n")
                        print("\t 0-Global basic configuration per channel.")
                        print("\t 1-Block per block configuration of each channel.")
                    Trimbreconfig = int(input())
                    if(Trimbreconfig == 1):
                        Number_Timbre_Channels = 3 #int(input())
                        for C in range(Number_Timbre_Channels):
                            if(DevMode!=1):
                                print(f"Set the blocks with timbre on the {ChannelsNames[C+1]} channel")
                            TimbreBlocks[C] = list(map(int, input().rstrip().split()))
                        for I in range(Number_Timbre_Channels):
                            NumTimbreBlocks = len(TimbreBlocks[I])
                            SetTrimbreConfig(Bank_Track, I, NumTimbreBlocks, ChannelsNames, TimbreBlocks, SQ1Timbres, SQ2Timbres, TRITimbres)
                    else:
                        if(DevMode!=1):
                            print("Set the global block with timbre on SQ1, SQ2 and TRI channels")
                        NumberBlock = int(input())
                        for C in range(3):        
                            TimbreBlocks[C].append(NumberBlock)
                        for I in range(3):
                            SetTrimbreConfig(Bank_Track, I, 1, ChannelsNames, TimbreBlocks, SQ1Timbres, SQ2Timbres, TRITimbres)
                    if(Trimbreconfig >= 0 and Trimbreconfig <=1):
                        break
                    else:
                        print("Error: Please select a valid option.")
                        ClearScreen()

                except ValueError:
                        print("Invalid entry. Please select a valid option.")
                        ClearScreen()
            if Number_Channels == 1:
                BlocksPerChannel = [(int(str(max(SQ1BlocksData)), 16))+1]
            elif Number_Channels == 2:
                BlocksPerChannel = [(int(str(max(SQ1BlocksData)), 16))+1,(int(str(max(SQ2BlocksData)), 16))+1]
            elif Number_Channels == 3:
                BlocksPerChannel = [(int(str(max(SQ1BlocksData)), 16))+1,(int(str(max(SQ2BlocksData)), 16))+1,(int(str(max(TRIBlocksData)), 16))+1]
            elif Number_Channels == 4:
                BlocksPerChannel = [(int(str(max(SQ1BlocksData)), 16))+1,(int(str(max(SQ2BlocksData)), 16))+1,(int(str(max(TRIBlocksData)), 16))+1,(int(str(max(NSEBlocksData)), 16))+1]
            elif Number_Channels == 5:
                BlocksPerChannel = [(int(str(max(SQ1BlocksData)), 16))+1,(int(str(max(SQ2BlocksData)), 16))+1,(int(str(max(TRIBlocksData)), 16))+1,(int(str(max(NSEBlocksData)), 16))+1,(int(str(max(NSEBlocksData)), 16))+1]
            start_row = FindRowDataSong(ftm, 'ROW_Number', 'PATTERN 00', ROWSong, start_row)
            BlocksChlNum = [SQ1BlocksData,SQ2BlocksData,TRIBlocksData,NSEBlocksData]
            NotesData = [] 
            #Create song data files
            print("Creating song data file...")
            with open(f"{Song_name_FILE}.asm", 'w') as SongFile:
                print("[....................]")
                NotesData = ReadData(ftm, start_row, BlocksPerChannel, Tempos[Bank_Track][Tempo_Track], NSE_dict, DMC_dict, NotesData)
                ClearScreen()
                print("Creating song data file...")
                print("[##########..........]")
                WriteData(SongFile, Number_Track, Number_Rows, TimbreBlocks, SQ1Timbres, SQ2Timbres, TRITimbres, ChannelsNames, BlocksChlNum, NotesData)
                ClearScreen()
                print("Creating song data file...")
                print("[####################]")
            print("***       Everything is ready to go        ***")
            print("***                                        ***")
            print("***          Thank you for using           ***")
            print("***               FTM2EBB                  ***")
            print("***                                        ***")
        except FileNotFoundError:
            print(f"Error: File '{ftmname}' does not exist.")
        except Exception as e:
            print(f"An error occurred during the conversion process: {e}")
