import numpy as np
import sys



def analyse_error_rate(ref, dut):
    assert ref.shape == dut.shape, f"Unequal sizes: {ref.shape} {dut.shape}"
    size = ref.shape[0]
    num_diff = np.count_nonzero(ref != dut)
    if num_diff == 0:
        print("Files identical")
        return
    bit_error_ppm = size / 1000000.0 * num_diff
    print(f"Total bytes: {size} ({size // (1024*1024)}MB), differing bytes: {num_diff}, Error PPM: {bit_error_ppm:.2f}")

    clusters = 0
    total_cluster_size = 0
    diff_counter = 0
    cluster_size_threshold = 16
    for idx in range(size):
        if ref[idx] != dut[idx]:
            if diff_counter == 0:
                clusters += 1
                diff_counter = cluster_size_threshold
            total_cluster_size += 1
        if diff_counter > 0:
            diff_counter -= 1

    average_cluster_size = total_cluster_size / clusters
    print(f"clusters: {clusters}, minimum gap {cluster_size_threshold}, ave_cluster_size: {average_cluster_size}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        assert False, f"usage: {sys.argv[0]} <ref.bin> <dut.bin>"
    ref = np.fromfile(sys.argv[1], dtype=np.uint8)
    dut = np.fromfile(sys.argv[2], dtype=np.uint8)

    analyse_error_rate(ref, dut)