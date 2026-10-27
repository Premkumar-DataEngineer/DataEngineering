from agents import trace, Runner, gen_trace_id
from planner_agent import planner_agent, WebSearchPlan, WebSearchItem
from search_agent import search_agent
from writer_agent import writer_agent, ReportData
import asyncio

class ResearchManager:
    async def run(self, query:str):
        """
        call the planner agent by passing the query to the planner agent
        Output of hte  planner agent feed to perform search function
        Output of the  perform search function is passed to the search agent
        Search agent output is passed to the  write agent
        :param query:
        :return:
        """
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            yield f"Starting the  Research Trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            search_plan=await self.plan_search(query)
            yield f"Number of searches performed {len(search_plan.search_items)}"
            search_result=await self.perform_search(search_plan)
            yield f"Search complete, Writing report..."
            report_data=await self.write_report(query, search_result)
            yield report_data.markdown_report
            
    async def plan_search(self, query:str)->WebSearchPlan:
        result=await Runner.run(planner_agent, query)
        return result.final_output

    async def search(self, websearch_item:WebSearchItem)->str|None:
        input_msg=f"Search term: {websearch_item.query}\nReason for searching: {websearch_item.reason}"
        result=await Runner.run(search_agent, input_msg)
        return result.final_output

    async def perform_search(self, websearch_plan:WebSearchPlan)->list[str]:
        tasks=[ self.search(search_item) for search_item in websearch_plan.search_items]
        return await asyncio.gather(*tasks)

    async def write_report(self,query:str, search:list[str])->ReportData:
        #frame the  input message to report
        input_message = f"Search term: {query}\nSummarized search result: {search}"
        #pass the  data to the  report writer agent
        result=await Runner.run(writer_agent, input_message)
        return result.final_output




if __name__=="__main__":
    RESEARCH_MANAGER=ResearchManager()
    query="Get the top self help books"
    async def main():
        async for result in RESEARCH_MANAGER.run(query):
            print(result)
    asyncio.run(main())

