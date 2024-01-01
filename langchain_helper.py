from langchain.llms import VertexAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

from sqlalchemy import create_engine, text

from few_shots import few_shots

# Function to get table info
def get_table_info(engine, table_name):
    with engine.connect() as connection:
        schema_query = text(f"SHOW CREATE TABLE {table_name}")
        schema_result = connection.execute(schema_query).fetchone()
        schema_info = f"Schema of {table_name}:\n{schema_result[1]}\n"

        sample_query = text(f"SELECT * FROM {table_name} LIMIT 3")
        sample_rows = connection.execute(sample_query).fetchall()
        sample_info = f"Sample rows from {table_name}:\n" + "\n".join(str(row) for row in sample_rows) + "\n"
    
    return schema_info + sample_info

def execute_sql_query(engine, query):
    with engine.connect() as connection:
        result = connection.execute(text(query)).fetchall()
        return result


def get_answer(question):
    db_user = "root"
    db_password = "root"
    db_host = "localhost"
    db_name = "chocolates"

    engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
    llm = VertexAI(temperature=0.2, max_output_tokens=1000)

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    to_vectorize = [" ".join(example.values()) for example in few_shots]
    vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)
    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=2,
    )
    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery"],
        template="Question: {Question}\nSQLQuery: {SQLQuery}"
    )
    prefix = "Please generate an SQL query depending on the question asked. You will be given all the table information. Use only the attibutes given in the table."
    suffix="Use only information from these tables: {table_info}:\nQuestion: {input}\nDo not use pre-amble\nSQLQuery:"

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=prefix,
        suffix=suffix,
        input_variables=["input", "table_info"],
    )
    table_info = get_table_info(engine, "discounts") + "\n" + get_table_info(engine, "chocolates")

    query_chain = LLMChain(llm=llm, prompt=few_shot_prompt)
    query = query_chain.run({"input": question, "table_info": table_info})
    print(query)
    result = execute_sql_query(engine, query)
   
    return result[0][0]

