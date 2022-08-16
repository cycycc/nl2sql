import yaml
import cohere
import streamlit as st
# from sql_formatter.core import format_sql
from google.cloud import bigquery

with open('./config.yaml') as f:
    config = yaml.full_load(f)

gen_config = config["gen"]
bq_config = config["bq"]

class NL2SQL:
    def __init__(self):
        self.debug = False
        # TODO: where should i put this?
        self.co = cohere.Client(gen_config['api_key'])
        self.model_id = gen_config['model_id']
        self.m_tokens = gen_config['max_tokens']
        self.temp = gen_config['temperature']
        self.k = gen_config['k']
        self.p = gen_config['p']
        self.freq_pen = gen_config['frequency_penalty']
        self.presence_pen = gen_config['presence_penalty']
        self.stop_seq = gen_config['stop_sequences']
        self.return_liki = gen_config['return_likelihoods']
        self.sep = gen_config['separator']

    def generate(self, final_nl_prompt):
        response = self.co.generate(
            model = self.model_id,
            prompt = final_nl_prompt,
            max_tokens = self.m_tokens,
            temperature = self.temp,
            k = self.k,
            p = self.p,
            frequency_penalty = self.freq_pen,
            presence_penalty = self.presence_pen,
            stop_sequences = self.stop_seq,
            return_likelihoods = self.return_liki)
        return self.clean_response(response)

    def clean_response(self, response):
        # might keep this around to do some post processing...
        return response.generations[0].text.strip('</s>')

class BigQuery:
    def __init__(self):
        self.client = bigquery.Client()

    def run_query(self, sql):
        query_job = self.client.query(sql)  # API request
        rows = query_job.result()  # Waits for query to finish
        return rows

class BigQueryStub:
    def run_query(self, sql):
        return [['STUB RESULT']]

# initialize the two classes
sql_generator = NL2SQL()
sql_runner = BigQuery()

# add a super cool title - hatching ckick always kills it
st.title('Natural Language 2 SQL :hatching_chick:')

st.markdown('## Prompt ##')
prompt = gen_config['prompt']
st.markdown(prompt)

# include a really slick text box for the user to put their query into
nl_query = st.text_input('Input Utterance', config["stream"]['default_input'])

# prepare the query!
nl_query = ' ' + nl_query.strip() + ' <s>'
final_nl_prompt =  prompt + nl_query

generate_sql_button = st.button('Generate SQL!')
generate_container = st.container()
if generate_sql_button:
    st.session_state.sql = ''
    st.session_state.rows = ''
    with generate_container:
        # if the user hits the generate button then we do these things

        # send natural language query to cohere
        # generate_container.markdown('### Sending your query to Cohere to generate SQL... ###')
        generate_container.markdown(final_nl_prompt)

        # call the generate endpoint
        with st.spinner(text='Generating SQL with Cohere :exploding_head:'):
            sql = sql_generator.generate(final_nl_prompt)
        # generate_container.markdown('## SQL has been generated :exploding_head: ##')

        # TODO: validate the sql
        table_name = prompt.split("<c>")[0].strip()
        sql = sql.replace(table_name, "`nl2sql." + table_name + "`")
        st.session_state.sql = sql

if 'sql' in st.session_state:
    generate_container.markdown(st.session_state.sql)

run_query_button = st.button('Run BigQuery with SQL')
query_container = st.container()
# not sure we need two buttons but added for the fun of it
if run_query_button:
    with query_container:
        # send cohere sql to BigQuery
        # query_container.markdown('### Sending SQL query to BigQuery :rocket: ###')

        # for testing
        # test_sql = bq_config['test_sql']

        with st.spinner(text='Sending SQL to BigQuery :rocket:'):
            st.session_state.rows = sql_runner.run_query(st.session_state.sql)

if 'rows' in st.session_state:
    # render the results to the user
    for row in st.session_state.rows:
        query_container.markdown(row[0])
