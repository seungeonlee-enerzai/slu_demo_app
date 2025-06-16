import gradio as gr
import os
import uuid
import soundfile as sf
import subprocess

# 오디오 저장 디렉토리
AUDIO_DIR = "./audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

def save_audio_to_wav(audio_path):
    """Gradio에서 받은 파일을 .wav로 저장하고 경로 반환"""
    try:
        data, samplerate = sf.read(audio_path)
        filename = f"recording_{uuid.uuid4().hex[:8]}.wav"
        save_path = os.path.join(AUDIO_DIR, filename)
        sf.write(save_path, data, samplerate)
        return save_path
    except Exception as e:
        return f"[ERROR] 오디오 저장 실패: {e}"

def run_process(audio_path):
    """외부 명령어 실행"""
    if not os.path.exists(audio_path):
        return "[ERROR] 유효한 오디오 파일이 없습니다."

    try:
        # 예시: 단순 echo 명령어 (실제로는 음성 인식 등 실행 가능)
        result = subprocess.run(
            ["echo", f"입력된 파일: {audio_path}"],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"[ERROR] 명령 실행 중 오류 발생: {e}"

with gr.Blocks(title="🎙️ 음성 녹음 데모") as demo:
    gr.Markdown("## 🎤 마이크로 음성을 녹음하고 프로세스를 실행해보세요!")

    
    audio_input = gr.Audio(label="마이크 녹음", type="filepath")
    record_button = gr.Button("📥 Record & Save")
    
    saved_path_text = gr.Textbox(label="저장된 파일 경로", interactive=False)

    run_button = gr.Button("▶️ Run")
    output_text = gr.Textbox(label="프로세스 결과", lines=4, interactive=False)

    def record_and_save(audio_file):
        save_path = save_audio_to_wav(audio_file)
        return save_path

    record_button.click(
        fn=record_and_save,
        inputs=[audio_input],
        outputs=[saved_path_text]
    )

    run_button.click(
        fn=run_process,
        inputs=[saved_path_text],
        outputs=[output_text]
    )

demo.launch()
