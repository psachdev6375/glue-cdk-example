import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'dbname', 'table', 'outputpath'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1734284151457 = glueContext.create_dynamic_frame.from_catalog(database=args['dbname'], table_name=args['table'], transformation_ctx="AWSGlueDataCatalog_node1734284151457")

# Script generated for node Change Schema
ChangeSchema_node1734284242537 = ApplyMapping.apply(frame=AWSGlueDataCatalog_node1734284151457, mappings=[("index", "string", "index", "string"), ("obf_flight_no", "string", "obf_flight_no", "string"), ("obf_departure", "string", "obf_departure", "string"), ("obf_opnl_prod_cd", "string", "obf_opnl_prod_cd", "string"), ("obf_ot_form_typ", "string", "obf_ot_form_typ", "string"), ("obf_act_ac_rgsn_cd", "string", "obf_act_ac_rgsn_cd", "string"), ("obf_act_dep_terminal_cd", "string", "obf_act_dep_terminal_cd", "string"), ("obf_section", "string", "obf_section", "string"), ("obf_sub_section", "string", "obf_sub_section", "string"), ("obf_quest_cd", "string", "obf_quest_cd", "string"), ("obf_quest_txt", "string", "obf_quest_txt", "string"), ("obf_quest_txt_nlts", "string", "obf_quest_txt_nlts", "string"), ("obf_month", "string", "obf_month", "string"), ("obf_date", "string", "obf_date", "string"), ("obf_brand", "string", "obf_brand", "string"), ("obf_rating", "string", "obf_rating", "string"), ("obf_answer", "string", "obf_answer", "string"), ("obf_personal_intro", "string", "obf_personal_intro", "string"), ("obf_pax_count", "string", "obf_pax_count", "string"), ("obf_pax_no_offer_meal", "string", "obf_pax_no_offer_meal", "string"), ("obf_pax_declined_meal", "string", "obf_pax_declined_meal", "string"), ("obf_monetary_value", "string", "obf_monetary_value", "string"), ("obf_description", "string", "obf_description", "string"), ("obf_action_taken", "string", "obf_action_taken", "string"), ("obf_further_action", "string", "obf_further_action", "string"), ("obf_hotel_name", "string", "obf_hotel_name", "string"), ("obf_room_number", "string", "obf_room_number", "string"), ("obf_specify_other", "string", "obf_specify_other", "string"), ("obf_seal_no_1", "string", "obf_seal_no_1", "string"), ("obf_seal_no_2", "string", "obf_seal_no_2", "string"), ("obf_bar_no", "string", "obf_bar_no", "string"), ("obf_trolley_no", "string", "obf_trolley_no", "string"), ("obf_tech_trolley_missing_items", "string", "obf_tech_trolley_missing_items", "string"), ("obf_catering_item", "string", "obf_catering_item", "string"), ("obf_actual_loaded", "string", "obf_actual_loaded", "string"), ("obf_suggested_loaded", "string", "obf_suggested_loaded", "string"), ("obf_pax_loaded", "string", "obf_pax_loaded", "string"), ("obf_insufficient_loaded", "string", "obf_insufficient_loaded", "string"), ("obf_excess_loaded", "string", "obf_excess_loaded", "string"), ("obf_seat_number", "string", "obf_seat_number", "string"), ("obf_station", "string", "obf_station", "string"), ("obf_chilled_stowage", "string", "obf_chilled_stowage", "string"), ("obf_stowage_affected", "string", "obf_stowage_affected", "string"), ("obf_stowage_affected_first", "string", "obf_stowage_affected_first", "string"), ("obf_stowage_affected_cw", "string", "obf_stowage_affected_cw", "string"), ("obf_stowage_affected_ce", "string", "obf_stowage_affected_ce", "string"), ("obf_stowage_affected_wt_plus", "string", "obf_stowage_affected_wt_plus", "string"), ("obf_stowage_affected_wt", "string", "obf_stowage_affected_wt", "string"), ("obf_stowage_affected_et", "string", "obf_stowage_affected_et", "string"), ("obf_stowage_affected_dom", "string", "obf_stowage_affected_dom", "string"), ("obf_stowage_affected_all", "string", "obf_stowage_affected_all", "string"), ("obf_num_of_meals", "string", "obf_num_of_meals", "string"), ("obf_ife_system", "string", "obf_ife_system", "string"), ("obf_customer_name", "string", "obf_customer_name", "string"), ("obf_reason", "string", "obf_reason", "string"), ("obf_iccm", "string", "obf_iccm", "string"), ("obf_feedback_sent_date", "string", "obf_feedback_sent_date", "string"), ("obf_faqs", "string", "obf_faqs", "string"), ("obf_faq_desc", "string", "obf_faq_desc", "string"), ("obf_comments", "string", "obf_comments", "string"), ("obf_service", "string", "obf_service", "string"), ("obf_pot_wat_lvl", "string", "obf_pot_wat_lvl", "string"), ("obf_pot_wat_ltrs", "string", "obf_pot_wat_ltrs", "string"), ("obf_source", "string", "obf_source", "string"), ("obf_aircraft", "string", "obf_aircraft", "string"), ("obf_aircraft_section", "string", "obf_aircraft_section", "string"), ("obf_author", "string", "obf_author", "string")], transformation_ctx="ChangeSchema_node1734284242537")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=ChangeSchema_node1734284242537, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1734284143136", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})

AmazonS3_node1734284253484 = glueContext.write_dynamic_frame.from_options(frame=ChangeSchema_node1734284242537, connection_type="s3", format="glueparquet", connection_options={"path": args['outputpath'], "partitionKeys": []}, format_options={"compression": "snappy"}, transformation_ctx="AmazonS3_node1734284253484")

job.commit()