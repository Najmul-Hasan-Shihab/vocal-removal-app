# Model Directory

Place your ONNX vocal separation model here.

## Required Model

Download `UVR-MDX-NET-Voc_FT.onnx` from:
https://github.com/TRvlvr/model_repo/releases

Place it in this directory so the path is:
`backend/models/UVR-MDX-NET-Voc_FT.onnx`

## Alternative Models

You can use other ONNX models for vocal separation. If using a different model:
1. Place the .onnx file in this directory
2. Update the model path in `backend/app.py` line 21
