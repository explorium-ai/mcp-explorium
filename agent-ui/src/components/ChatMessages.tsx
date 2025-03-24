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
  partial_json: string;
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
                {message.content.map((content, contentIndex) => {
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

                  // We only show the "Using tool" message if it's the last message
                  const isLastMessage =
                    index === messages.length - 1 &&
                    contentIndex === message.content.length - 1;
                  if (aiMessage.type === "tool_use" && isLastMessage) {
                    return (
                      <UsingToolMessage
                        key={aiMessage.index}
                        toolName={aiMessage.name}
                        partialJson={aiMessage.partial_json}
                      />
                    );
                  }
                })}
              </div>
            );
          }

          if (message.type === "tool" && !!message.name) {
            // We shouldn't show the tool message if:
            // - Its name is "autocomplete"
            // - There is another "autocomplete" tool message after it
            if (
              message.name === "autocomplete" &&
              index < messages.length - 1
            ) {
              const nextMessage = messages[index + 1];
              if (
                nextMessage?.type === "tool" &&
                nextMessage.name === "autocomplete"
              ) {
                return null;
              }
            }
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
    <div className="max-w-2/3 w-fit py-2 px-3 bg-[#286167] rounded ml-auto my-4">
      <div className="break-words text-white">{content}</div>
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
function getUsingToolMessage(toolName: MCPToolName, partialJson = ""): string {
  if (toolName === "autocomplete") {
    try {
      const parsedJson = JSON.parse(partialJson);
      return `Thinking about ${parsedJson.field}`;
    } catch {
      // Try to extract field from partial JSON
      if (partialJson.includes('"field"')) {
        try {
          // Extract field value using regex
          const fieldMatch = partialJson.match(/"field"\s*:\s*"([^"]+)"/);
          if (fieldMatch && fieldMatch[1]) {
            return `Thinking about ${fieldMatch[1]}`;
          }
        } catch {
          return "Thinking";
        }
      }
      return "Thinking";
    }
  }

  const messages: { [key: string]: string } = {
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

  return messages[toolName] || "Working on it";
}

function UsingToolMessage({
  toolName,
  partialJson,
}: {
  toolName: MCPToolName;
  partialJson: string;
}) {
  return (
    <div className="flex items-center gap-2 my-4 h-8">
      <LoaderCircle className="animate-spin w-4 text-gray-600" />
      <div className="text-sm text-gray-600 italic">
        {getUsingToolMessage(toolName, partialJson)}
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
      const enrichments = (parsedContent.results as any[])?.length;
      if (!enrichments) {
        return "Found 0 results";
      }
      if (enrichments === 1) {
        return "Found 1 result";
      }
      return `Found ${enrichments} results`;
    }
    case "create_search_session": {
      const parsedContent = JSON.parse(content);
      return `Found ${parsedContent.session_details.total_results} results`;
    }
    case "session_fetch_events": {
      return "Found events";
    }
    case "autocomplete": {
      return "Created search filters";
    }
  }
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
