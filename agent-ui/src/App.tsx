"use client";

import { useStream } from "@langchain/langgraph-sdk/react";
import type { Message } from "@langchain/langgraph-sdk";
import useExploriumStore from "@/store";
import ApiKeyInput from "@/components/ApiKeyInput";

export default function App() {
  const apiKey = useExploriumStore((state) => state.apiKey);
  const thread = useStream<{ messages: Message[] }>({
    apiUrl: "http://localhost:2024",
    assistantId: "research_agent",
    messagesKey: "messages",
  });

  if (!apiKey) {
    return <ApiKeyInput />;
  }

  return (
    <div>
      <div>
        {thread.messages.map((message) => {
          if (message.type === "tool") {
            console.log(message);
          }
          if (message.type === "ai") {
            if (Array.isArray(message.content)) {
              return message.content.map((content, index) => {
                if (content.type === "text") {
                  return (
                    <div key={`${message.id}-${index}`}>{content.text}</div>
                  );
                }
                return null;
              });
            }
            return <div key={message.id}>{message.content as string}</div>;
          }
          return <div key={message.id}>{message.content as string}</div>;
        })}
      </div>

      <form
        onSubmit={(e) => {
          e.preventDefault();

          const form = e.target as HTMLFormElement;
          const message = new FormData(form).get("message") as string;

          form.reset();

          console.log("apiKey", apiKey);

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
        }}
      >
        <input type="text" name="message" />

        {thread.isLoading ? (
          <button key="stop" type="button" onClick={() => thread.stop()}>
            Stop
          </button>
        ) : (
          <button key="send" type="submit">
            Send
          </button>
        )}
      </form>
    </div>
  );
}
