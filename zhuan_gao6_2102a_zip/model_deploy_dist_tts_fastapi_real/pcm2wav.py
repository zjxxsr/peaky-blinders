from util import compose_wav_header

if '__main__' == __name__:

    with open('./demo.pcm', 'rb') as f:
        audio = f.read()
        header = compose_wav_header(len(audio), 1, 16, 16000)
        with open('./demo.wav', 'wb') as fo:
            fo.write(header)
            fo.write(audio)

    print('All OK')
