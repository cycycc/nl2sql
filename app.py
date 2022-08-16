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
        self.prompt = gen_config['prompt']
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

    def generate(self, nl_query):
        response = self.co.generate(
            model = self.model_id,
            prompt = self.prompt + nl_query,
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
        return response.generations[0].text

class BigQuery:
    def __init__(self):
        self.client = bigquery.Client()

    def run_query(self, sql):
        query_job = self.client.query(sql)  # API request
        rows = query_job.result()  # Waits for query to finish
        return rows

# initialize the two classes
sql_generator = NL2SQL()
sql_runner = BigQuery()

# add a super cool title - hatching ckick always kills it
st.title('Natural Language 2 SQL :hatching_chick:')

# include a really slick text box for the user to put their query into
nl_query = st.text_input('Input Utterance', 'how many times is the fuel propulsion is cng?')

# prepare the query!
nl_query = ' ' + nl_query.strip().lower() + ' <s>'

generate_sql_button = st.button('Generate SQL!')

run_query_button = st.button('Run BigQery with SQL')

# if the user hits the generate button then we do these things
if generate_sql_button:

    # send natural language query to cohere
    sql_gen_state = st.text('## Sending your query to Cohere to generate SQL... ###')
    # call the generate endpoint
    sql = sql_generator.generate(nl_query)
    sql_gen_state.markdown('## SQL has been generated :exploding_head: ##')

    # TODO: validate the sql
    # sql_formatted = format_sql(sql)

    st.markdown(sql)

# not sure we need two buttons but added for the fun of it
if run_query_button:
    # send cohere sql to BigQuery
    query_state = st.markdown('### Sending SQL query to BigQuery :rocket: ###')

    # for testing
    test_sql = bq_config['test_sql']

    rows = sql_runner.run_query(test_sql)

    # render the results to the user
    for row in rows:
        st.markdown(row[0])

if st.checkbox('Show Prompt'):
    st.markdown('## Prompt ##')
    st.markdown(sql_generator.prompt)
