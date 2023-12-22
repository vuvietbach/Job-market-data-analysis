python topic_modelling.py --col_name benefits --save_dir large_files/benefits_model --result_save_dir normalized_data/benefits
python topic_modelling.py --col_name description --save_dir large_files/desc_model --result_save_dir normalized_data/description

python get_topic_info.py --col_name requirements --model_dir large_files/req_model --output_dir normalized_data/requirements
python get_topic_info.py --col_name benefits --model_dir large_files/benefits_model --output_dir normalized_data/benefits
python get_topic_info.py --col_name description --model_dir large_files/desc_model --output_dir normalized_data/description

python analyze_topic.py --col_name requirements --topic_prediction_path normalized_data/requirements/topic_prediction.json --topic_info_path normalized_data/requirements/topic_info.json
python analyze_topic.py --col_name description --topic_prediction_path normalized_data/description/topic_prediction.json --topic_info_path normalized_data/description/topic_info.json