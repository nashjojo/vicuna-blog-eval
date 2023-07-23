answer_csv := ../human_sense/2023-06-23_LLM_eval_humansense_data_searchgpt_0.4.csv
baseline_model := GPT-4\:website
model_id := searchgpt_0.4

rating:
	python3 -u eval/jsonl2csv.py \
		--output_file eval/table/review/${model_id}/review_${baseline_model}_${model_id}.csv \
		--input_file eval/table/review/${model_id}/review_${baseline_model}_${model_id}.jsonl

judge: 
	mkdir -p eval/table/review/${model_id} ; \
	python3 -u eval/eval_gpt_review.py -q eval/table/question_human_sense.jsonl -a eval/table/answer/answer_human_sense_${baseline_model}.jsonl eval/table/answer/answer_human_sense_${model_id}.jsonl -p eval/table/prompt.jsonl -r eval/table/reviewer.jsonl -o eval/table/review/${model_id}/review_${baseline_model}_${model_id}.jsonl | tee log_${model_id} ; \
	while true ; do \
		python3 -u eval/eval_gpt_review.py -q eval/table/question_human_sense.jsonl -a eval/table/answer/answer_human_sense_${baseline_model}.jsonl eval/table/answer/answer_human_sense_${model_id}.jsonl -p eval/table/prompt.jsonl -r eval/table/reviewer.jsonl -o eval/table/review/${model_id}/review_${baseline_model}_${model_id}_new.jsonl -e eval/table/review/${model_id}/review_${baseline_model}_${model_id}.jsonl | tee -a log_${model_id} ; \
		mv eval/table/review/${model_id}/review_${baseline_model}_${model_id}_new.jsonl eval/table/review/${model_id}/review_${baseline_model}_${model_id}.jsonl ; \
		if grep -q "eval_finished" log_${model_id}; then \
			break ; \
		fi ; \
	done

answer: $(answer_csv)
	python3 eval/qa_csv2jsonl.py --input_file $(answer_csv) \
		--question eval/table/question_human_sense.jsonl ; \
	python3 eval/qa_csv2jsonl.py --input_file $(answer_csv) \
		--answer eval/table/answer/answer_human_sense_${baseline_model}.jsonl \
		--model_ids ${baseline_model} ; \
	python3 eval/qa_csv2jsonl.py --input_file $(answer_csv) \
		--answer eval/table/answer/answer_human_sense_${model_id}.jsonl \
		--model_ids ${model_id} ; \
