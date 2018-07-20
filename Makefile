b=$(base)
q=$(quote)
t1=$(unix_time)
dt=$(interval)
t2=$(shell echo $$(( $(unix_time) + $(interval) )))

/home/fbuonerba/log_returns_data/log_return_b_q_t1_t2.txt: /home/fbuonerba/exchange_rates_data/exchange_rate_b_q_t1.txt /home/fbuonerba/exchange_rates_data/exchange_rate_b_q_t2.txt
	python3 compute_log_returns.py $(t1) $(b) $(q) $(dt)

/home/fbuonerba/exchange_rates_data/exchange_rate_b_q_t1.txt:
	python3 upload_rates.py $(t1) $(b) $(q) 

/home/fbuonerba/exchange_rates_data/exchange_rate_b_q_t2.txt:
	python3 upload_rates.py $(t2) $(b) $(q) 



