import numpy as np
import sys
from numpy import zeros, hstack
from aubio import source, pitch


def cough_detect(your_file):
    cough_flag = 0 
    # Setting parameters for the microphone data
    win_s = 4096
    # This variable modifies how many times the frequency is calculated per second
    hop_s = 512
    # M5Stack's microphone samplerate
    samplerate = 22050

    s = source(your_file, samplerate, hop_s)
    samplerate = s.samplerate

    tolerance = 0.8

    # Use Spectral auto-correlation density algorithm for pitch detection
    pitch_o = pitch("specacf", win_s, hop_s, samplerate)
    # Setting the units to Hertz
    pitch_o.set_unit("Hz")
    pitch_o.set_tolerance(tolerance)

    pitches = []
    confidences = []

    total_frames = 0
    while True:
        samples, read = s()
        pitchaa = pitch_o(samples)[0]
        pitches += [pitchaa]
        confidence = pitch_o.get_confidence()
        confidences += [confidence]
        total_frames += read
        if read < hop_s: break

    # The list of frequencies is in np.array(pitches)

    # We will calculate the avg frequency by adding the frequencies/ticks
    suma = 0
    tick = 0
    # The counter for ticks will be stored in this array
    ticksCount = []
    # The average frequencies will be stored in this arrays
    means = []

    for k in np.array(pitches):
        # It filters frequencies beyond 1000 because coughs are within 100 to 900 hz
        if k > 0 and k < 1000:
            tick += 1
            suma += k

        # The frequencies and the ticks will be considered part of a continuous sound
        # If they are in betwwen two ticks with 0 frequency
        elif k == 0 and tick != 0:
            # Append the anumber of ticks the sound lasted
            ticksCount.append(tick)
            # Calculates the average frequency and appends it to the means list
            means.append(suma/tick)

            # Reset the values for the next continuous sounds
            tick = 0
            k = 0
            suma = 0



    # For every continuous sound
    for x in range(len(means)):
        '''consider it a cough in the recording if:
        frequency between 300 and 900 hz
        duration between 14 and 60 ticks'''
        if means[x] > 300 and means[x] < 900 and ticksCount[x] >= 14 and ticksCount[x] <= 60:
            c += 1
            # Breaks after one cough is recorded
            break

    return cough_flag

def threshold(c, m, cough_flag):
    questionnaire_flag = 0
    m += 5/60 #add 5 seconds to the time counter


    #Do nothing if there is less than 5 minutes between the previous cough or if there is none
    if m < 5 or cough_flag == 0:
        return c, m, questionnaire_flag
    #if more than 5 minutes passed, count it
    else:
        q = c*((0.5)**(m/30)) #calculate the function just before the cough
        q += 1 #add 1 because of the cough

        if q > 2.25:
            questionnaire_flag = 1
            return 0, 0, questionnaire_flag #return the questionnaire flag set to 1
        else:
            return q, 0, questionnaire_flag #reset the minutes since the last cough


questionnaire_flag = 0
v = 0

while questionnaire_flag == 0:
    #name of the file
    your_file = f"audio{str(v)}.wav"

    cough_flag = cough_detect(your_file)
    c, m, questionnaire_flag = threshold(c, m, cough_flag)

#signal m5 to prompt questionaire

