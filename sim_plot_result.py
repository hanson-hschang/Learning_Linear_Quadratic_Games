from sim_parameters import *

memory_length = temp_algo_params["memory_length"]
tau1 = temp_algo_params["tau1"]
tau2 = temp_algo_params["tau2"]
M1 = temp_algo_params["M1"]
M2 = temp_algo_params["M2"]
epsilon1 = temp_algo_params["epsilon1"]
epsilon2 = temp_algo_params["epsilon2"]

signature  = str(memory_length) + "_" + str(tau1) + "_" + str(tau2) + "_" + str(M1) + "_" + str(M2) \
                    + "_" + str(epsilon1) + "_" + str(epsilon2)


initial_val_dir = "initial_values_set" + str(temp_algo_params["initial_values_index"]) + "/" 
benchmark_initial_dir = "initial_values_set" + str(temp_algo_params["initial_values_index"]) + "/benchmark_algo/" 


if temp_algo_params["exact_inner_loop"]:
    # dir = initial_val_dir + "exact_inner_sol/"
    if temp_algo_params["outer_loop_model_free"]:
        dir = initial_val_dir + "exact_inner_sol/estimated_outer_grad/"
        benchmark_dir = benchmark_initial_dir + "exact_inner_sol/estimated_outer_grad/"

    else: 
        dir = initial_val_dir + "exact_inner_sol/exact_outer_grad/"
        benchmark_dir = benchmark_initial_dir + "exact_inner_sol/exact_outer_grad/"

elif temp_algo_params["inner_loop_model_free"]:
    # dir = initial_val_dir + "estimated_inner_grad/"
    if temp_algo_params["outer_loop_model_free"]:
        dir = initial_val_dir + "estimated_inner_grad/estimated_outer_grad/"
        benchmark_dir = benchmark_initial_dir + "estimated_inner_grad/estimated_outer_grad/"
    else: 
        dir = initial_val_dir + "estimated_inner_grad/exact_outer_grad/"
        benchmark_dir = benchmark_initial_dir + "estimated_inner_grad/exact_outer_grad/"

else: 
    # dir = initial_val_dir + "exact_inner_grad/"
    if temp_algo_params["outer_loop_model_free"]:
        dir = initial_val_dir + "exact_inner_grad/estimated_outer_grad/"
        benchmark_dir = benchmark_initial_dir + "exact_inner_grad/estimated_outer_grad/"
    else: 
        dir = initial_val_dir + "exact_inner_grad/exact_outer_grad/"
        benchmark_dir = benchmark_initial_dir + "exact_inner_grad/estimated_outer_grad/"

ind = 0

cost_list_filename = dir + "cost_list/" + signature + "_" + str(ind) + ".pk"
cost_diff_filename = dir + "cost_diff_list/" + signature + "_" + str(ind) + ".pk"
lambda_list_filename = dir + "lambda_list/" + signature + "_" + str(ind) + ".pk"
avg_ng_list_filename = dir + "avg_ng_list/" + signature + "_" + str(ind) + ".pk"

# benchmark algo list filenames
benchmark_cost_list_filename = benchmark_dir + "cost_list/" + signature + "_" + str(ind) + ".pk"
benchmark_cost_diff_filename = benchmark_dir + "cost_diff_list/" + signature + "_" + str(ind) + ".pk"
benchmark_lambda_list_filename = benchmark_dir + "lambda_list/" + signature + "_" + str(ind) + ".pk"
benchmark_avg_ng_list_filename = benchmark_dir + "avg_ng_list/" + signature + "_" + str(ind) + ".pk"
benchmark_KL_list_filename = benchmark_dir + "KL_list/" + signature + "_" + str(ind) + ".pk"

benchmark_cost_filename = "benchmarks/" + "cost.pk"
benchmark_lambda_filename = "benchmarks/" + "lambda.pk"

# cost_list_file = open(cost_list_filename, "rb")
# cost_diff_file = open(cost_diff_filename, "rb")
# lambda_list_file = open(lambda_list_filename, "rb")
# avg_ng_list_file = open(avg_ng_list_filename, "rb")

benchmark_cost_list_file = open(benchmark_cost_list_filename, "rb")
benchmark_cost_diff_file = open(benchmark_cost_diff_filename, "rb")
benchmark_lambda_list_file = open(benchmark_lambda_list_filename, "rb")
benchmark_avg_ng_list_file = open(benchmark_avg_ng_list_filename, "rb")
benchmark_KL_list_file = open(benchmark_KL_list_filename, "rb")

benchmark_cost_file = open(benchmark_cost_filename, "rb")
benchmark_lambda_file = open(benchmark_lambda_filename, "rb")

# temp_cost_list = pickle.load(cost_list_file)
# temp_cost_diff_list = pickle.load(cost_diff_file)
# temp_lambda_list = pickle.load(lambda_list_file)
# temp_avg_ng_list = pickle.load(avg_ng_list_file)

benchmark_cost_list = pickle.load(benchmark_cost_list_file)
benchmark_cost_diff_list = pickle.load(benchmark_cost_diff_file)
benchmark_lambda_list = pickle.load(benchmark_lambda_list_file)
benchmark_avg_ng_list = pickle.load(benchmark_avg_ng_list_file)
benchmark_KL_list = pickle.load(benchmark_KL_list_file)

nash_cost = pickle.load(benchmark_cost_file)
nash_lambda = pickle.load(benchmark_lambda_file)

benchmark_K_list = benchmark_KL_list["K_list"]
benchmark_L_list = benchmark_KL_list["L_list"]

from riccati_equation import Riccati
riccati = Riccati(temp_model_params)
matrix_K_time_trajectory = riccati.get_gain_K_time_trajectory()

# Already plotted the linear convergence part
plt.rcParams['text.usetex'] = True
# plot linear convergence

fig = plt.figure()
axes = fig.subplots(riccati.u_dim, riccati.x_dim)
for iter_number in range(memory_length):
    if (iter_number + 1) % int(memory_length/4) == 0 or iter_number == 0:
        K_list_at_iter_number = np.zeros((horizon_length, temp_model_params['control_dim1'], temp_model_params['x_dim']))
        for time_step in range(horizon_length):
            K_list_at_iter_number[time_step] = benchmark_K_list[iter_number][time_step].numpy()
        # print(K_list_at_iter_number)
        for i in range(riccati.u_dim):
            for j in range(riccati.x_dim):
                axes[i, j].plot(K_list_at_iter_number[:, i, j], linestyle='--', label='iter no. :'+str(iter_number+1))

for i in range(riccati.u_dim):
    for j in range(riccati.x_dim):
        axes[i, j].plot(matrix_K_time_trajectory[:, i, j], color='black', label='Riccati' )
    
axes[0, 1].legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), ncol=6)

plt.show()