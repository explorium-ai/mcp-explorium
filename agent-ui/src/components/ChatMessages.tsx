import { Message } from "@langchain/langgraph-sdk";
import React from "react";
import { MCPToolName } from "./ai/toolTypes";
import { Check, Frown, LoaderCircle, X } from "lucide-react";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { cn } from "@/lib/utils";

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

  let lastHumanMessage = "";

  return (
    <div className="flex-1 overflow-y-auto py-2 gap-2 flex flex-col">
      <div className="w-[748px] mx-auto">
        {messages.map((message, index) => {
          const isPlaceholder = message.id === "placeholder";
          if (message.type === "human") {
            if (isPlaceholder && lastHumanMessage === message.content) {
              return null;
            }

            lastHumanMessage = message.content as string;
            return (
              <HumanMessage
                key={message.id}
                content={message.content as string}
                placeholder={isPlaceholder}
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

function HumanMessage({
  content,
  placeholder,
}: {
  content: string;
  placeholder?: boolean;
}) {
  return (
    <div
      className={cn(
        "max-w-2/3 w-fit py-2 px-3 bg-[#286167] rounded ml-auto my-4",
        placeholder && "opacity-80"
      )}
    >
      <div className="break-words text-white">{content}</div>
    </div>
  );
}

function AssistantMessage({ content }: { content: string }) {
  return (
    <div className="pr-8">
      <Markdown
        remarkPlugins={[remarkGfm]}
        components={{
          // Custom table rendering
          table: (props) => (
            <table className="border-collapse table-auto w-full my-4 bg-white text-sm shadow">
              {props.children}
            </table>
          ),
          thead: (props) => (
            <thead className="border-explorium-table-border">
              {props.children}
            </thead>
          ),
          th: (props) => (
            <th className="border border-explorium-table-border px-6 py-3 text-left font-normal text-[#7F8583] min-w-[150px]">
              {props.children}
            </th>
          ),
          td: (props) => (
            <td className="border border-explorium-table-border px-6 py-3 align-text-top whitespace-normal">
              {Array.isArray(props.children)
                ? props.children.map((child) => {
                    if (typeof child === "string") {
                      return (
                        <div className="mb-1">
                          {child.replace("<br>", "\n")}
                        </div>
                      );
                    }
                    return child;
                  })
                : props.children}
            </td>
          ),

          // Custom list rendering
          ul: (props) => (
            <ul className="list-disc pl-6 my-4">{props.children}</ul>
          ),
          ol: (props) => (
            <ol className="list-decimal pl-6 my-4">{props.children}</ol>
          ),
          li: (props) => (
            <li className="my-1 marker:text-black/60 marker:text-sm">
              {props.children}
            </li>
          ),
        }}
      >
        {content}
      </Markdown>
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
          // Extract fmiield value using regex
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
    create_company_research_session: "Matching",
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
    <div className="flex items-center gap-2 my-4 h-8 animate-in fade-in">
      <LoaderCircle className="animate-spin w-4 text-gray-600" />
      <div className="text-sm text-gray-600 italic">
        {getUsingToolMessage(toolName, partialJson)}
      </div>
    </div>
  );
}

function getUsedToolMessage(
  toolName: MCPToolName,
  content: any
): { text: string; type: "warning" | "success" } {
  switch (toolName) {
    case "create_company_research_session": {
      const parsedContent = JSON.parse(content);
      const totalResults = parsedContent.session_details.total_results;
      if (totalResults === 0) {
        return { text: "No companies found", type: "warning" };
      }
      if (totalResults === 1) {
        return { text: "Matched company", type: "success" };
      }
      return { text: `Matched ${totalResults} companies`, type: "success" };
    }
    case "session_enrich": {
      const parsedContent = JSON.parse(content);
      const enrichments = (parsedContent.results as any[])?.length;
      if (!enrichments) {
        return { text: "No enrichments found", type: "warning" };
      }
      if (enrichments === 1) {
        return { text: "Found 1 result", type: "success" };
      }
      return { text: `Found ${enrichments} results`, type: "success" };
    }
    case "create_search_session": {
      const parsedContent = JSON.parse(content);
      return {
        text: `Found ${
          parsedContent.session_details.total_results || 0
        } results`,
        type: "success",
      };
    }
    case "session_fetch_events": {
      const parsedContent = JSON.parse(content);
      if (parsedContent.total_events === 0) {
        return { text: "No events found", type: "warning" };
      }
      return {
        text: `Found ${parsedContent.total_events} events`,
        type: "success",
      };
    }
    case "session_view_data": {
      const parsedContent = JSON.parse(content);
      return {
        text: `Loaded ${Object.keys(parsedContent).length} results`,
        type: "success",
      };
    }
    case "autocomplete": {
      return { text: "Created search filters", type: "success" };
    }
  }
  return { text: "Done", type: "success" };
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
  const isError = !success || gotError(content);
  const { text, type } = isError
    ? { text: "Something went wrong", type: "warning" }
    : getUsedToolMessage(toolName, content);

  return (
    <div className="flex items-center gap-2 my-4 h-8">
      {isError ? (
        <>
          <X className="w-4 h-4 text-red-500" />
          <div className="text-sm text-gray-600 italic">
            Something went wrong
          </div>
        </>
      ) : (
        <>
          {type === "success" && (
            <div className="flex items-center justify-center bg-explorium-green rounded-full w-3 h-3 aspect-square mx-0.5 animate-in zoom-in">
              <Check className="w-4 h-4 translate-x-0.5 -translate-y-[1px]" />
            </div>
          )}
          {type === "warning" && <Frown className="w-4 h-4 text-gray-600" />}
          <div className="text-sm text-gray-600 italic animate-in slide-in-from-left-2 animation">
            {text}
          </div>
        </>
      )}
    </div>
  );
}
