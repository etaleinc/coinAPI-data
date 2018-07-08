/home/fbuonerba/log_returns_data/log_return_$(base)_$(quote)_$(unix_time)_$(shell echo $$(( $(unix_time) + $(interval) ))).txt: /home/fbuonerba/exchange_rates_data/exchange_rate_$(base)_$(quote)_$(unix_time).txt /home/fbuonerba/exchange_rates_data/exchange_rate_$(base)_$(quote)_$(shell echo $$(( $(unix_time) + $(interval) ))).txt
	python3 compute_log_returns.py $(unix_time) $(base) $(quote) $(interval)

/home/fbuonerba/exchange_rates_data/exchange_rate_$(base)_$(quote)_$(unix_time).txt:
	python3 upload_rates.py $(unix_time) $(base) $(quote)

/home/fbuonerba/exchange_rates_data/exchange_rate_$(base)_$(quote)_$(shell echo $$(( $(unix_time) + $(interval) ))).txt:
	python3 upload_rates.py $(shell echo $$(( $(unix_time) + $(interval) ))) $(base) $(quote)



