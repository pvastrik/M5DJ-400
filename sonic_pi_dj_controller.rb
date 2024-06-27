# Welcome to Sonic Pi
samples = ["C:/Users/priid/kool/IoT/muss/elvis.mp3",
           "C:/Users/priid/kool/IoT/muss/lady.mp3",
           "C:/Users/priid/kool/IoT/muss/looking.mp3",
           "C:/Users/priid/kool/IoT/muss/ndn.mp3"]
use_bpm 140
step = 1
idx = 1
with_fx :hpf do |h|
  with_fx :lpf do |l|
    with_fx :ixi_techno do |f|
      ##| s = synth :prophet, note: 40, sustain: 60*60
      ##| sample "C:/Users/priid/kool/IoT/everything/bass.wav"
      control h, mix: 0
      control l, mix: 0
      control f, mix: 0
      s1 = sample samples[0]
      s2 = sample samples[1], amp: 0
      live_loop :foo do
        use_real_time
        high, low, echo = sync "/osc*/trigger/effects"
        control h, mix: high
        control l, mix: low
        control f, mix: 1-echo
        trig, val = sync "/osc*/trigger/fader"
        print step
        if step == 1
          if trig <= -1
            control s2, amp: 0.2
            idx = (idx + 1) % 4
            
            step = 2
          end
        else
          if step == 2
            if trig > 0.2
              control s2, amp: trig
              control s1, amp: 1.2-trig
              if trig >= 1
                step = 3
                kill s1
                s1 = sample samples[idx], amp: 0
                idx = (idx + 1) % 4
                
              end
            end
          else
            if step == 3
              if trig <= -1
                control s1, amp: 0.2
                step = 4
              end
            else
              if step == 4
                if trig > 0.2
                  control s1, amp: trig
                  control s2, amp: 1.2-trig
                  if trig >= 1
                    step = 1
                    kill s2
                    s2 = sample samples[idx], amp: 0
                    idx = (idx + 1) % 4
                  end
                end
              end
            end
          end
        end
      end
    end
  end
  
  
end
