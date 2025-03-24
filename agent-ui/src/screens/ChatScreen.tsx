import ChatEmptyState from "@/components/ChatEmptyState";
import ChatInput from "@/components/ChatInput";
import ChatMessages from "@/components/ChatMessages";
import useExploriumStore from "@/store";
import { Message } from "@langchain/langgraph-sdk";
import { useStream } from "@langchain/langgraph-sdk/react";
import { useCallback, useEffect, useState } from "react";

export default function ChatScreen() {
  const thread = useStream<{ messages: Message[] }>({
    apiUrl: import.meta.env.VITE_AGENT_API_URL,
    assistantId: "research_agent",
    messagesKey: "messages",
  });
  const [placeholderMessage, setPlaceholderMessage] = useState<string | null>(
    null
  );
  const apiKey = useExploriumStore((state) => state.apiKey);

  const onSendMessage = useCallback(
    (message: string) => {
      try {
        setPlaceholderMessage(message);
        thread.submit(
          { messages: [{ type: "human", content: message }] },
          {
            config: {
              configurable: {
                explorium_api_key: apiKey,
              },
            },
          }
        );
      } catch (error) {
        console.error("Error submitting message", error);
      }
    },
    [thread, apiKey]
  );

  useEffect(() => {
    // Check if the last human message is the same as the placeholder message
    if (
      thread.messages?.length &&
      thread.messages[thread.messages.length - 1].type === "human" &&
      thread.messages[thread.messages.length - 1].content === placeholderMessage
    ) {
      setPlaceholderMessage(null);
    }
  }, [thread.messages, placeholderMessage, setPlaceholderMessage]);

  return (
    <div className="mx-auto h-full flex flex-col pb-4">
      <div className="flex-1 overflow-y-auto">
        {thread.messages?.length === 0 && !placeholderMessage ? (
          <ChatEmptyState />
        ) : (
          <ChatMessages
            messages={[
              ...(thread.messages ?? []),
              ...(placeholderMessage
                ? [
                    {
                      id: "placeholder",
                      type: "human",
                      content: placeholderMessage,
                    } satisfies Message,
                  ]
                : []),
            ]}
          />
        )}
      </div>
      <div className="w-[768px] mx-auto">
        <ChatInput onSubmit={onSendMessage} disabled={thread.isLoading} />
      </div>
    </div>
  );
}
