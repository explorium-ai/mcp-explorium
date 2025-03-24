import ChatEmptyState from "@/components/ChatEmptyState";
import ChatInput from "@/components/ChatInput";
import ChatMessages from "@/components/ChatMessages";
import useExploriumStore from "@/store";
import { Message } from "@langchain/langgraph-sdk";
import { useStream } from "@langchain/langgraph-sdk/react";
import { useCallback } from "react";

export default function ChatScreen() {
  const thread = useStream<{ messages: Message[] }>({
    apiUrl: import.meta.env.VITE_AGENT_API_URL,
    assistantId: "research_agent",
    messagesKey: "messages",
  });
  const apiKey = useExploriumStore((state) => state.apiKey);

  const onSendMessage = useCallback(
    (message: string) => {
      try {
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

  return (
    <div className="mx-auto h-full flex flex-col pb-4">
      <div className="flex-1 overflow-y-auto">
        {thread.messages?.length === 0 ? (
          <ChatEmptyState />
        ) : (
          <ChatMessages messages={thread.messages ?? []} />
        )}
      </div>
      <div className="w-[768px] mx-auto">
        <ChatInput onSubmit={onSendMessage} disabled={thread.isLoading} />
      </div>
    </div>
  );
}
