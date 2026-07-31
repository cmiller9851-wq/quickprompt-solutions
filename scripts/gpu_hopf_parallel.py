# To execute on NVIDIA GPU, install cupy (e.g., pip install cupy-cuda12x)
# and replace numpy with cupy below.
import numpy as np
import time

def evaluate_parallel_hopf_holonomy_gpu(num_trajectories: int = 100_000, steps: int = 1000):
    """
    Simulates thousands of parallel Non-Abelian gauge trajectories on S3 
    mapped to S2 via Hopf Fibration on GPU hardware.
    """
    print(f"Initializing {num_trajectories:,} parallel trajectories over {steps} steps...")
    
    # 1. State Allocation: Allocate (4, N) matrix for unit quaternions on VRAM/Memory
    # Quaternion array structure: [w, x, y, z]
    states = np.zeros((4, num_trajectories), dtype=np.float64)
    states[0, :] = 1.0  # Initial state: [1, 0, 0, 0]
    
    # Generate random trajectory frequency profiles for each parallel path
    freq_x = np.random.uniform(0.5, 2.0, num_trajectories)
    freq_y = np.random.uniform(0.5, 2.0, num_trajectories)
    freq_z = np.random.uniform(0.5, 2.0, num_trajectories)

    dt = (2.0 * np.pi) / steps
    
    start_time = time.time()

    # 2. Parallel Time Integration Loop
    for i in range(steps):
        t = i * dt
        
        # Calculate instantaneous gauge potential components across all trajectories
        wx = np.sin(freq_x * t) * 0.5
        wy = np.cos(freq_y * t) * 0.5
        wz = np.sin(freq_z * t) * 0.5
        
        # Magnitude of angular velocity vector
        w_mag = np.sqrt(wx**2 + wy**2 + wz**2)
        d_theta = w_mag * (dt / 2.0)
        
        # Incremental Quaternions (dq) for all threads simultaneously
        sin_factor = np.where(d_theta > 1e-12, np.sin(d_theta) / w_mag, 0.0)
        
        dq_w = np.cos(d_theta)
        dq_x = wx * sin_factor
        dq_y = wy * sin_factor
        dq_z = wz * sin_factor
        
        # Hamilton Multiplication in Parallel
        # w = w1*w2 - x1*x2 - y1*y2 - z1*z2
        # x = w1*x2 + x1*w2 + y1*z2 - z1*y2 ...
        w_new = states[0]*dq_w - states[1]*dq_x - states[2]*dq_y - states[3]*dq_z
        x_new = states[0]*dq_x + states[1]*dq_w + states[2]*dq_z - states[3]*dq_y
        y_new = states[0]*dq_y - states[1]*dq_z + states[2]*dq_w + states[3]*dq_x
        z_new = states[0]*dq_z + states[1]*dq_y - states[2]*dq_x + states[3]*dq_w
        
        # Renormalize states across GPU threads
        norm = np.sqrt(w_new**2 + x_new**2 + y_new**2 + z_new**2)
        states[0, :] = w_new / norm
        states[1, :] = x_new / norm
        states[2, :] = y_new / norm
        states[3, :] = z_new / norm

    # 3. Parallel Hopf Fibration Projection pi: S3 -> S2
    # S2 Vector = [2(xz + wy), 2(yz - wx), w^2 + z^2 - x^2 - y^2]
    w, x, y, z = states[0], states[1], states[2], states[3]
    s2_x = 2.0 * (x * z + w * y)
    s2_y = 2.0 * (y * z - w * x)
    s2_z = w**2 + z**2 - x**2 - y**2

    execution_time = time.time() - start_time
    
    # Statistics across all GPU threads
    mean_s2_z = float(np.mean(s2_z))
    std_s2_z = float(np.std(s2_z))

    print(f"--- GPU EXECUTION COMPLETE ---")
    print(f"Total Trajectories Processed : {num_trajectories:,}")
    print(f"Execution Time              : {execution_time:.4f} seconds")
    print(f"Mean Final S2 Z-Projection   : {mean_s2_z:.6f}")
    print(f"Projection Variance (StdDev) : {std_s2_z:.6f}")

if __name__ == "__main__":
    evaluate_parallel_hopf_holonomy_gpu(num_trajectories=100_000, steps=1000)
