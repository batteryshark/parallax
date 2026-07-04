# RSRC.GPU: GPU Compute Access

## Description

Accessing GPU compute capabilities through CUDA, OpenCL, Metal, Vulkan compute shaders, WebGPU compute, DirectCompute, or GPU-accelerated ML frameworks. The atom describes code that dispatches general-purpose computation to the GPU, not code that uses the GPU exclusively for rendering or display. Includes loading GPU compute kernels, allocating GPU memory, dispatching compute workgroups, and transferring data between host and device memory.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | CUDA kernel launches (`<<<blocks, threads>>>`), OpenCL `clEnqueueNDRangeKernel`, Vulkan `vkCmdDispatch`, Metal `commandEncoder.dispatchThreadgroups`, WebGPU compute pipeline creation, ML framework GPU device selection (`torch.cuda`, `tf.device('/gpu:0')`) |
| Static Binary | Partial | CUDA runtime or driver API imports, OpenCL/Vulkan/Metal compute function imports, PTX or SPIR-V compute shader bytecode embedded in binary sections |
| Runtime/Dynamic | Yes | GPU utilization on compute-capable devices, GPU memory allocation, GPU driver API calls, GPU kernel execution in profiler traces, elevated GPU power consumption |

## Disambiguation

- **vs legitimate ML/graphics**: GPU access is expected in ML frameworks, graphics engines, video processing pipelines, and scientific computing libraries. RSRC.GPU applies to the hardware access pattern regardless of purpose. A TensorFlow training loop, a Blender render pass, and a cryptocurrency miner all exhibit RSRC.GPU, context determines interpretation.
- **vs RSRC.CPU**: Some workloads can run on either CPU or GPU. RSRC.GPU applies when computation is explicitly dispatched to the GPU. If a library dynamically selects CPU or GPU based on hardware availability, both atoms may apply depending on the execution path.

## Structural Relationships

- **Often co-occurs with**: `RSRC.CPU` (host-side orchestration of GPU workloads), `SYSI.HW` (querying GPU capabilities, VRAM, compute units), `NETW.*` (transmitting GPU computation results externally), `ENVI.ENVCHECK` (checking for GPU presence before dispatching)
- **May imply**: GPU driver and runtime dependencies, elevated power consumption, GPU memory allocation separate from host memory

## Notes

The key structural data points are: which GPU compute API is used, what kernel or shader is dispatched, whether the code queries for GPU hardware before dispatching, and where the computation output goes. Code that checks for GPU availability and falls back to CPU is structurally different from code that requires GPU presence. Whether the GPU compute is reachable from the package's documented public API or only from internal/hidden code paths is an important structural property.
