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

#ifndef MS_KERNELS_INTERNAL_KERNEL_MATMUL_MATMUL_IMPL_H_
#define MS_KERNELS_INTERNAL_KERNEL_MATMUL_MATMUL_IMPL_H_

#include "asdops/op_desc.h"
#include "asdops/operation.h"
#include "asdops/run_info.h"
#include "asdops/tactic.h"
#include "asdops/tensor.h"

#include "utils.h"
#include "backend_param.h"
#include "param/matmul_ext_param.h"
#include "matmul_common/pp_matmul_info.h"
#include "matmul_common/tiling_utils.h"
#include "matmul_common/tiling_data.h"
#include "matmul_common/pp_matmul_common_tiling.h"
#include "tune_repo/utils.h"
#include "internal_kernel.h"

#include "acl_rt.h"
#include <unordered_map>

namespace mindspore {
namespace internal {

using namespace tiling;

enum class MatMulAlgo { PP = 0, LLM_CUSTOM = 1 };

class MatMulImpl : public InternelKernelImpl {
 public:
  MatMulImpl(const OpParamPtr &param) : InternelKernelImpl(param){};
  virtual ~MatMulImpl() = default;
  bool Init(const ValidateInfo &info) override;
  void SetDeviceTilingBuf(const DeviceRawBuf &tilingBuf) override;
  int Launch() override;
  size_t GetTilingBufSize() override;
  int Tiling(HostRawBuf &tilingBuf) override;
  void TilingBasicFromPp(uint32_t &blockDim, PpTilingData &tilingdata);
  int TilingPp(HostRawBuf &tilingBuf, uint64_t tilingId, const uint32_t &blockDim, const PpTilingData &tilingdata);
  int TilingLLMCustom(HostRawBuf &tilingBuf, uint64_t tilingId, const uint32_t &blockDim,
                      const PpTilingData &tilingdata);
  std::vector<uint64_t> GetWorkSpaceSize() override;
  int InferShape(const std::vector<DIMS> &input_shapes, std::vector<DIMS> &output_shapes) override;
  bool UseCustomMatMul();
  void GetTunedKey();
  void SetTunedValueCustom(const std::vector<int> &tuned_config);

 private:
  uint32_t m_, k_, n_;
  const char *func_name_ = "UnknownFunc";
  MatMulAlgo algo_ = MatMulAlgo::PP;
  DeviceRawBuf tiling_addr_;
  std::string soc_{"Ascend910B2"};
  HardwareInfo hwInfo_;
  CustomMatmulTilingData t_;
  std::vector<int> tune_key_;
  REPO tuningTable_;
  REPO tuningTableCustom_;
  TensorDType input_dtype_;
  TensorDType output_dtype_;
  int block_dim_ = 0;
  bool trans_a_{false};
  bool trans_b_{true};
};

}  // namespace internal
}  // namespace mindspore
#endif
