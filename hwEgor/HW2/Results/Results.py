import matplotlib.pyplot as plt


#Average 10 tests with 500 reqests

pure_socket_server = 19989.09566242137
pure_socket_server_with_cpu_bound = 149.45903291553202

select_server = 16555.19050638297
select_server_with_cpu_bound = 144.3775488864005

selectors_server = 11384.989170025092
selectors_server_with_cpu_bound = 136.27887564257628

http_server = 215.72835864444576
http_server_with_cpu_bound = 92.04084788388803

list_request_response_result = [pure_socket_server, select_server, selectors_server, http_server]

list_request_response_result_with_cpu_bound = [pure_socket_server_with_cpu_bound, select_server_with_cpu_bound,
                                               selectors_server_with_cpu_bound, http_server_with_cpu_bound]

x = ["pure_socket_server" ,"select_server", "selectors_server", "http_server"]

plt.figure(figsize=(12, 4))


plt.subplot(1, 2, 1)
plt.title("request_response_result")
plt.plot(x, list_request_response_result, '-')
plt.plot(x, list_request_response_result, 'go')

plt.subplot(1, 2, 2)
plt.title("request_response_result_with_cpu_bound")
plt.plot(x, list_request_response_result_with_cpu_bound, '--')
plt.plot(x, list_request_response_result_with_cpu_bound, 'go')

#plt.show()
plt.savefig('saved_figure.png')