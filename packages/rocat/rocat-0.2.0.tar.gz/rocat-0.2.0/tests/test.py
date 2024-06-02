import olefile
import struct

def get_ppt_text(file_path):
    try:
        ole = olefile.OleFileIO(file_path)
        print("OLE file opened successfully")

        # PowerPoint Document 스트림 찾기
        ppt_stream = None
        for stream in ole.listdir():
            if stream[0] == "PowerPoint Document":
                ppt_stream = stream
                break

        if ppt_stream is None:
            raise Exception("PowerPoint Document stream not found")

        print(f"PowerPoint Document stream found: {ppt_stream}")

        # 텍스트 추출
        text_data = []
        stream_data = ole.openstream(ppt_stream).read()

        # RecordHeader 구조체 언패킹
        header_fmt = "<HH"
        header_size = struct.calcsize(header_fmt)

        current_offset = 0
        while current_offset < len(stream_data):
            rec_header = stream_data[current_offset:current_offset+header_size]
            rec_type, rec_len = struct.unpack(header_fmt, rec_header)

            if rec_type == 0x0FA0:  # RT_TextCharsAtom
                text_bytes = stream_data[current_offset+header_size:current_offset+header_size+rec_len]
                text = text_bytes.decode('utf-16-le', errors='ignore')
                text_data.append(text)
            elif rec_type == 0x0FA8:  # RT_TextBytesAtom
                text_bytes = stream_data[current_offset+header_size:current_offset+header_size+rec_len]
                text = text_bytes.decode('latin-1', errors='ignore')
                text_data.append(text)
            elif rec_type == 0x0F9F:  # RT_TextHeaderAtom
                current_offset += header_size + rec_len
                continue

            current_offset += header_size + rec_len

        # 추출된 텍스트 후처리
        cleaned_text = "\n".join(text_data).strip()

        return cleaned_text
    except Exception as e:
        return f"ERROR: {str(e)}"

if __name__ == "__main__":
    ppt_text = get_ppt_text("test.ppt")
    print(ppt_text)