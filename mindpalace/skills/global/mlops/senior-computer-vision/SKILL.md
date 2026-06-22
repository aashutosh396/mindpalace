---
name: Senior Computer Vision Engineer
description: Use when building object detection pipelines, training custom vision models, optimizing inference, or deploying vision systems — YOLO/Faster R-CNN/DETR, segmentation, ONNX/TensorRT, dataset prep.
tags: [computer-vision, object-detection, yolo, faster-rcnn, detr, segmentation, onnx, tensorrt, quantization, dataset-prep]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/senior-computer-vision
---

# Senior Computer Vision Engineer

Production CV: detection, segmentation, deployment. Stack: PyTorch/torchvision/timm, Ultralytics/Detectron2/MMDetection, ONNX/TensorRT/OpenVINO/CoreML.

## Workflow 1: Detection Pipeline
1. **Requirements**: target classes, real-time FPS, speed-vs-accuracy, deployment target, dataset size.
2. **Architecture**:
   - Real-time (>30 FPS) → YOLOv8/v11, RT-DETR (single-stage).
   - High accuracy → Faster R-CNN, DINO (two-stage).
   - Small objects → YOLO + SAHI, Faster R-CNN + FPN.
   - Edge → YOLOv8n, MobileNetV3-SSD.
   - Transformer end-to-end (no NMS) → DETR, DINO, RT-DETR.
3. **Dataset**: convert to COCO (recommended), 0.8/0.1/0.1 split, verify with pycocotools.
4. **Train + validate** on test set.
5. **Evaluate**: mAP@50 >0.7, mAP@50:95 >0.5, precision/recall >0.8, inference <33ms for 30 FPS.

## Workflow 2: Optimization & Deployment
1. Benchmark baseline (batch 1/4/8/16, warmup, iterations).
2. Path by target: NVIDIA cloud → ONNX → TensorRT FP16; NVIDIA edge → TensorRT INT8; Intel → OpenVINO; Apple → CoreML; mobile → TFLite/ONNX Mobile.
3. Export ONNX (dynamic batch, simplify), verify with `onnx.checker`.
4. Quantization tradeoff: FP16 = 50% size, 1.5-2x speed, <0.5% accuracy drop; INT8 = 25% size, 2-4x speed, 1-3% drop (needs calibration data).
5. Convert to runtime (`trtexec --fp16`, `mo`, coremltools), benchmark vs baseline (expect ~3.5x with TensorRT FP16, ~-0.3% mAP).

## Workflow 3: Dataset Prep
Audit raw (sizes, formats, corrupted, duplicates, class distribution) → clean (remove corrupted/dupes) → convert format (VOC/YOLO/LabelMe/CVAT → COCO) → augment (geometric: flip/rotate/scale; color: brightness/hue/blur; advanced: mosaic/mixup/cutout) → stratified split (seed 42) → generate config (YOLO data.yaml / Detectron2). Split: <1K → 70/15/15, 1-10K → 80/10/10, >10K → 90/5/5.

## Architecture Selection
Detection speed/accuracy: YOLOv8n 1.2ms/37.3mAP (edge) → YOLOv8x 10.1ms/53.9mAP (max) · RT-DETR-L 5.3ms/53.0 (no NMS) · Faster R-CNN R50 46ms/40.2 · DINO 85ms/49.0. Segmentation: YOLOv8-seg 4.5ms (real-time instance), Mask R-CNN 67ms (quality masks), SAM 50ms (zero-shot), SegFormer 15ms (efficient semantic). CNN needs 1-10K images/fast training; ViT needs 10-100K+/slow but excellent global context.

## Performance Targets
Real-time: >30 FPS, mAP@50 >0.6, P99 <50ms, <4GB GPU, <50MB. Edge: >15 FPS, >0.5 mAP, <100ms, <2GB, <20MB.
