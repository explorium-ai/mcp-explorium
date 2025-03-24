import { Message } from "@langchain/langgraph-sdk";
import React from "react";
import { MCPToolName } from "./ai/toolTypes";
import { Check, LoaderCircle, X } from "lucide-react";

interface ChatMessagesProps {
  messages: Message[];
}

interface AiTextMessage {
  type: "text";
  index: number;
  text: string;
}

interface AiUsingToolMessage {
  type: "tool_use";
  index: number;
  name: MCPToolName;
}

type AiMessage = AiTextMessage | AiUsingToolMessage;

export default function ChatMessages({ messages }: ChatMessagesProps) {
  console.log("messages", messages);

  // Add ref for the messages container
  const messagesEndRef = React.useRef<HTMLDivElement>(null);

  // Scroll to bottom whenever messages change
  React.useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto py-2 gap-2 flex flex-col">
      <div className="w-[748px] mx-auto">
        {messages.map((message, index) => {
          const isLastMessage = index === messages.length - 1;
          if (message.type === "human") {
            return (
              <HumanMessage
                key={message.id}
                content={message.content as string}
              />
            );
          }

          if (message.type === "ai" && Array.isArray(message.content)) {
            return (
              <div key={message.id}>
                {message.content.map((content) => {
                  const aiMessage = content as AiMessage;
                  // Assistant text messages
                  if (aiMessage.type === "text") {
                    return (
                      <AssistantMessage
                        key={aiMessage.index}
                        content={aiMessage.text}
                      />
                    );
                  }

                  // "Using tool" messages
                  if (aiMessage.type === "tool_use" && isLastMessage) {
                    return <UsingToolMessage toolName={aiMessage.name} />;
                  }
                })}
              </div>
            );
          }

          if (message.type === "tool" && !!message.name) {
            return (
              <UsedToolMessage
                key={message.id}
                toolName={message.name as MCPToolName}
                content={message.content as string}
                success={message.status === "success"}
              />
            );
          }
        })}
      </div>
      <div ref={messagesEndRef} />
    </div>
  );
}

function HumanMessage({ content }: { content: string }) {
  return (
    <div className="max-w-2/3 w-fit py-2 px-3 bg-explorium-green rounded ml-auto my-4">
      <div className="break-words">{content}</div>
    </div>
  );
}

function AssistantMessage({ content }: { content: string }) {
  return (
    <div className="pr-8">
      <div className="break-words whitespace-pre-wrap">{content}</div>
    </div>
  );
}

const usingToolMessages: { [key: string]: string } = {
  get_search_filters: "Setting up Explorium search",
  create_search_session: "Searching for companies",
  create_company_research_session: "Researching specific companies",
  get_session_details: "Reading through the results",
  session_load_more_results: "Loading more results",
  session_view_data: "Looking at the data",
  get_business_id: "Getting business ID",
  session_enrich: "Getting more information",
  session_fetch_events: "Searching for events",
};

function UsingToolMessage({ toolName }: { toolName: MCPToolName }) {
  return (
    <div className="flex items-center gap-2 my-4 h-8">
      <LoaderCircle className="animate-spin w-4 text-gray-600" />
      <div className="text-sm text-gray-600 italic">
        {usingToolMessages[toolName]}
      </div>
    </div>
  );
}

function getUsedToolMessage(toolName: MCPToolName, content: any): string {
  switch (toolName) {
    case "create_company_research_session":
      return "Researched companies";
    case "session_enrich": {
      const parsedContent = JSON.parse(content);
      const enrichments = (parsedContent.results as any[]).length;
      if (enrichments === 1) {
        return "Got more information";
      }
      return `Got ${enrichments} enrichments`;
    }
    case "create_search_session": {
      const parsedContent = JSON.parse(content);
      return `Found ${parsedContent.session_details.total_results} results`;
    }
    case "session_fetch_events": {
      return "Found events";
    }
  }
  console.log("content", { content });
  return "Done";
}

function gotError(content: string): boolean {
  if (!content || typeof content !== "string" || content.length === 0) {
    return true;
  }
  const parsedContent = JSON.parse(content);
  if (parsedContent.error) {
    return true;
  }
  return false;
}

function UsedToolMessage({
  toolName,
  content,
  success,
}: {
  toolName: MCPToolName;
  content: string;
  success: boolean;
}) {
  return (
    <div className="flex items-center gap-2 my-4 h-8">
      {!success || gotError(content) ? (
        <>
          <X className="w-4 h-4 text-red-500" />
          <div className="text-sm text-gray-600 italic">
            Something went wrong
          </div>
        </>
      ) : (
        <>
          <div className="flex items-center justify-center bg-explorium-green rounded-full w-3 h-3 aspect-square mx-0.5">
            <Check className="w-4 h-4 translate-x-0.5 -translate-y-[1px]" />
          </div>
          <div className="text-sm text-gray-600 italic">
            {getUsedToolMessage(toolName, content)}
          </div>
        </>
      )}
    </div>
  );
}
