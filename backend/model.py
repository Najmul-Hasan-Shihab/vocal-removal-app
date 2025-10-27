import subprocess
import os
import shutil
import soundfile as sf
import numpy as np

class VocalSeparator:
    def __init__(self):
        """
        Initialize Demucs-based separator
        Demucs is a state-of-the-art music source separation model
        """
        pass
    
    def _convert_to_wav(self, input_path: str, output_path: str):
        """Convert audio file to WAV format using pydub"""
        from pydub import AudioSegment
        
        # Load audio file
        audio = AudioSegment.from_file(input_path)
        
        # Export as WAV
        audio.export(output_path, format="wav")
        
        return output_path
    
    def separate(self, file_path: str, out_vocals_path: str, out_instrumental_path: str):
        """
        Separate vocals from instrumental in an audio file using Demucs
        
        Args:
            file_path: Path to input audio file
            out_vocals_path: Path to save vocals
            out_instrumental_path: Path to save instrumental (accompaniment)
            
        Returns:
            Tuple of (vocals_path, instrumental_path)
        """
        # Get the output directory
        output_dir = os.path.dirname(out_vocals_path)
        
        # Convert to WAV first if not already WAV (to avoid FFmpeg dependency)
        wav_file = file_path
        temp_wav = None
        if not file_path.lower().endswith('.wav'):
            try:
                temp_wav = os.path.join(output_dir, 'temp_input.wav')
                self._convert_to_wav(file_path, temp_wav)
                wav_file = temp_wav
            except Exception as e:
                print(f"Could not convert to WAV: {e}")
                # Continue with original file and hope for the best
        
        # Run Demucs separation
        # -n htdemucs: use the hybrid transformer demucs model (best quality)
        # --two-stems=vocals: only separate vocals and accompaniment (faster)
        # -o: output directory
        # --mp3: output as MP3 to avoid torchcodec WAV saving issues
        # --mp3-bitrate=320: high quality MP3
        try:
            result = subprocess.run(
                ['python', '-m', 'demucs', '--two-stems=vocals', '--mp3', '--mp3-bitrate=320', '-o', output_dir, wav_file],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            print(f"Demucs stdout: {result.stdout}")
            print(f"Demucs stderr: {result.stderr}")
            print(f"Demucs return code: {result.returncode}")
            
            if result.returncode != 0:
                raise Exception(f"Demucs failed with code {result.returncode}: {result.stderr}")
            
            # Demucs creates: output_dir/htdemucs/filename/vocals.mp3 and no_vocals.mp3
            base_name = os.path.splitext(os.path.basename(wav_file))[0]
            demucs_output_dir = os.path.join(output_dir, 'htdemucs', base_name)
            
            print(f"Looking for outputs in: {demucs_output_dir}")
            
            vocals_source = os.path.join(demucs_output_dir, 'vocals.mp3')
            instrumental_source = os.path.join(demucs_output_dir, 'no_vocals.mp3')
            
            print(f"Vocals source: {vocals_source}, exists: {os.path.exists(vocals_source)}")
            print(f"Instrumental source: {instrumental_source}, exists: {os.path.exists(instrumental_source)}")
            
            # Move files to desired locations
            # Convert MP3 to WAV for output
            if os.path.exists(vocals_source):
                # Copy as-is (MP3) or convert to WAV
                if out_vocals_path.endswith('.wav'):
                    # Convert MP3 to WAV
                    from pydub import AudioSegment
                    audio = AudioSegment.from_mp3(vocals_source)
                    audio.export(out_vocals_path, format="wav")
                else:
                    shutil.copy2(vocals_source, out_vocals_path)
            else:
                raise Exception(f"Vocals file not found: {vocals_source}")
            
            if os.path.exists(instrumental_source):
                # Copy as-is (MP3) or convert to WAV
                if out_instrumental_path.endswith('.wav'):
                    # Convert MP3 to WAV
                    from pydub import AudioSegment
                    audio = AudioSegment.from_mp3(instrumental_source)
                    audio.export(out_instrumental_path, format="wav")
                else:
                    shutil.copy2(instrumental_source, out_instrumental_path)
            else:
                raise Exception(f"Instrumental file not found: {instrumental_source}")
            
            # Clean up Demucs output directory
            demucs_base = os.path.join(output_dir, 'htdemucs')
            if os.path.exists(demucs_base):
                shutil.rmtree(demucs_base)
            
            # Clean up temp WAV file
            if temp_wav and os.path.exists(temp_wav):
                os.unlink(temp_wav)
            
            return out_vocals_path, out_instrumental_path
            
        except subprocess.TimeoutExpired:
            raise Exception("Processing timeout - file may be too large")
        except Exception as e:
            # Clean up temp file on error
            if temp_wav and os.path.exists(temp_wav):
                try:
                    os.unlink(temp_wav)
                except:
                    pass
            raise Exception(f"Separation failed: {str(e)}")
