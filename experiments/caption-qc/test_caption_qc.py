from caption_qc import inspect_srt

def test():
    good = '1\n00:00:00,000 --> 00:00:03,000\nHello world.\n'
    assert inspect_srt(good)['finding_count'] == 0
    with open('sample.srt', encoding='utf-8') as f:
        report = inspect_srt(f.read())
    codes = {i['code'] for i in report['findings']}
    assert {'overlap', 'line_length', 'reading_speed', 'duration', 'empty_text'} <= codes, codes
    assert report['cue_count'] == 4
    print('PASS: clean caption + synthetic error cases', report['finding_count'], 'findings')

if __name__ == '__main__':
    test()
