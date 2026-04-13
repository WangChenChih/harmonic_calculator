import numpy as np

class harmonic:
    
    def __init__(self, open_string_pitch, open_string_octave):
        self.open_string_pitch = open_string_pitch
        self.open_string_octave = open_string_octave
        pitch_list = ["C", "C_sharp", "D", "D_sharp", "E", "F", "F_sharp", "G", "G_sharp", "A", "A_sharp", "B"]
        self.pitch_list = pitch_list
        self.semi = 2 ** (1/12)
        return
    
    def freq_from_pitch(self, name, oct):
        """
        Turn a pitch name and octave into a frequency multiplier. 
        For example, the pitch name of C4 is C and the octave is 4, so the frequency multiplier would be 1 * (2 ** 4) = 16.
        """

        semi = self.semi

        if name == "C":
            f = 1
        elif name == "C_sharp" or name == "D_flat":
            f = semi
        elif name == "D":
            f = semi ** 2
        elif name == "D_sharp" or name == "E_flat":
            f = semi ** 3
        elif name == "E":
            f = semi ** 4
        elif name == "F":
            f = semi ** 5
        elif name == "F_sharp" or name == "G_flat":
            f = semi ** 6
        elif name == "G":
            f = semi ** 7
        elif name == "G_sharp" or name == "A_flat":
            f = semi ** 8
        elif name == "A":
            f = semi ** 9
        elif name == "A_sharp" or name == "B_flat":
            f = semi ** 10
        elif name == "B":
            f = semi ** 11
        else:
            raise ValueError("Invalid pitch name")

        return f * (2 ** oct)
    
    def pitch_add(self, pitch_name, octave, semitone_add, output_is_string = True):
        """
        The output is the note that is semitone higher than the input note. For example, if the input note is C4 and the semitone is 2, the output note would be D4.
        """
        semi = self.semi
        name_index = self.pitch_list.index(pitch_name)
        name_new = self.pitch_list[(name_index + semitone_add) % 12]
        oct_new = octave + (name_index + semitone_add) // 12
        if output_is_string:
            return name_new + str(oct_new)
        else:
            return name_new, oct_new

    def pitch_from_freq(self, freq):
        """
        Turn the value of frequency multiplier into pitch name and octave. For example, if the frequency multiplier is 16, the pitch name would be C and the octave would be 4.
        """
        semi = self.semi
        oct = int(np.log2(freq))
        name_index = int(np.round(np.log2(freq / (2 ** oct)) / np.log2(semi)))
        name = self.pitch_list[name_index]
        return name, oct
    
    def pitch_list_new_base(self, pitch_name_base):
        """
        Generate a new pitch list, where the first element is pitch_name_base.
        """
        if pitch_name_base == "D_flat":
            pitch_name_base = "C_sharp"
        elif pitch_name_base == "E_flat":
            pitch_name_base = "D_sharp"
        elif pitch_name_base == "G_flat":
            pitch_name_base = "F_sharp"
        elif pitch_name_base == "A_flat":
            pitch_name_base = "G_sharp"
        elif pitch_name_base == "B_flat":
            pitch_name_base = "A_sharp"
        
        name_index = self.pitch_list.index(pitch_name_base)
        pitch_list_new = self.pitch_list[name_index:] + self.pitch_list[:name_index]
        return pitch_list_new
    
    def calculate_artificial_harmonic(self, pitch_name_goal, octave_goal, oct_tolerance = 1, freq_tolerance = 0.01):
        """
        For erhu, the artificial harmonic is produced by pressing the string tightly using forefinger at a certain note [pitch_1, octave_1], and lightly touch the string using another finger at another note [pitch_2, octave_2].
        We will search the possible combinations of the output pitch name for producing the desired note. However, since the longest possible distance our fingers can reach is at most 6 semitones, we will only search for the combinations in such a range. 
        Moreover, if octave_1 is too high relative to the open string, it will be difficult to find the position of the note in practice, so we will only search octave_1 within 2 octaves by default.
        
        The requirement for note_1 and note_2 is that f_goal / f_1 = n and f_goal / f_2 = n-1, where n must be an integer.
        However, since the frequency multiplier is not perfectly accurate, we will allow a small tolerance for the frequency multiplier. For example, if n is 2, then f_goal / f_1 should be close to 2, and f_goal / f_2 should be close to 1.5. We will allow a tolerance of 0.01 for both of these ratios.
        """
        f_goal = self.freq_from_pitch(name=pitch_name_goal, oct=octave_goal)

        # the first two for-loops: find the position for the forefinger
        for oct in range(oct_tolerance):
            for semi_add_1 in range(1,11+1):
                pitch_1, octave_1 = self.pitch_add(pitch_name=self.open_string_pitch, octave=self.open_string_octave, semitone_add=semi_add_1, output_is_string=False)
                f_1 = self.freq_from_pitch(name=pitch_1, oct=octave_1)
                
                # condition 1
                if if_int(num= f_goal / f_1, tolerance=freq_tolerance):
                    deter_int = int_part(f_goal / f_1)
                else:
                    continue
                
                # find the position for the second finger
                for semi_add_2 in range(1,6+1):
                    pitch_2, octave_2 = self.pitch_add(pitch_name=pitch_1, octave=octave_1, semitone_add=semi_add_2, output_is_string=False)
                    f_2 = self.freq_from_pitch(name=pitch_2, oct=octave_2)
                    
                    # condition 2
                    if if_int(num= f_goal / f_2, tolerance=freq_tolerance) and int_part(f_goal / f_2) == int(deter_int - 1):
                        print("forefinger: " + pitch_1+str(octave_1+oct) + " , " + "pinkie: " + pitch_2+str(octave_2+oct))
                    else:
                        continue
    
    def calculate_natural_harmonic(self, pitch_name_goal, octave_goal, freq_tolerance = 0.01):
        """
        The highest possible frequency of the natural harmonic is an octave higher than the open-string frequency. 
        The condition is f_goal / f_0 = n
        """
        f_goal = self.freq_from_pitch(name=pitch_name_goal, oct=octave_goal)

        for semi_add in range(1,11+1):
            pitch_0, octave_0 = self.pitch_add(pitch_name=self.open_string_pitch, octave=self.open_string_octave, semitone_add=semi_add, output_is_string=False)
            f_0 = self.freq_from_pitch(name=pitch_0, oct=octave_0)

            if if_int(num= f_goal / f_0, tolerance=freq_tolerance):
                print("position: "+ pitch_0+str(octave_0))
                    
def int_part(num):
    # round off
    if np.abs(num - int(num)) < 0.5:
        return int(num)
    else:
        return int(num) + 1

def if_int(num, tolerance):
    if np.abs(int_part(num=num) - num) >= tolerance:
        return False
    else:
        return True