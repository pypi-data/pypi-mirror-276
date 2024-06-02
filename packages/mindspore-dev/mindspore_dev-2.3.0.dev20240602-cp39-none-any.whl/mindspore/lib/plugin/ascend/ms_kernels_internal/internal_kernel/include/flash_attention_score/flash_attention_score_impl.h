/**
 * Copyright 2023-2024 Huawei Technologies Co., Ltd
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef MS_KERNELS_INTERNAL_KERNEL_FLASHATTENTION_IMPL_H_
#define MS_KERNELS_INTERNAL_KERNEL_FLASHATTENTION_IMPL_H_

#include "asdops/op_desc.h"
#include "asdops/operation.h"
#include "asdops/run_info.h"
#include "asdops/tactic.h"
#include "asdops/tensor.h"

#include "internal_kernel.h"
#include "param/attention_param.h"
#include "acl_rt.h"

#include <unordered_map>

namespace mindspore {
namespace internal {
class FlashAttentionScoreImpl : public InternelKernelImpl {
 public:
  FlashAttentionScoreImpl(const OpParamPtr &param) : InternelKernelImpl(param){};
  virtual ~FlashAttentionScoreImpl() = default;
  bool Init(const ValidateInfo &info) override;
  void SetInputs(const std::vector<Tensor *> &inputs) override;
  void SetOutputs(const std::vector<Tensor *> &outputs) override;
  void SetWorkSpace(const std::vector<DeviceRawBuf> &workspace) override;
  void SetStream(const void *stream_ptr) override;
  void SetDeviceTilingBuf(const DeviceRawBuf &tilingBuf) override;
  int Launch() override;
  size_t GetTilingBufSize() override;
  int Tiling(HostRawBuf &tilingBuf) override;
  std::vector<uint64_t> GetWorkSpaceSize() override;
  int InferShape(const std::vector<DIMS> &input_shapes, std::vector<DIMS> &output_shapes) override;

 private:
  uint64_t B, N, Q_S, KV_S, D, G, CORE_NUM;
  int inner_precise, pre_tokens, next_tokens, sparse_mode;
  bool BFLOAT16, BSH, ALIBI, AMASK;
  const std::vector<Tensor *> *inputs_;
  const std::vector<Tensor *> *outputs_;
  void *stream_ptr_ = nullptr;
  void *workspace_addr = nullptr;
  void *tiling_addr_ = nullptr;
};

}  // namespace internal
}  // namespace mindspore

#endif
