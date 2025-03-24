import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";
import { useEffect, useRef } from "react";

interface ChatInputProps {
  onSubmit: (message: string) => void;
  disabled: boolean;
}

export default function ChatInput({ onSubmit, disabled }: ChatInputProps) {
  const inputRef = useRef<HTMLTextAreaElement>(null);
  useEffect(() => {
    if (!disabled && inputRef.current) {
      inputRef.current.focus();
    }
  }, [disabled]);

  return (
    <form
      className="relative"
      onSubmit={(e) => {
        e.preventDefault();
        const form = e.target as HTMLFormElement;
        const message = new FormData(form).get("message") as string;
        onSubmit?.(message);
        form.reset();
      }}
    >
      <Textarea
        ref={inputRef}
        className="resize-none h-24 pt-2 px-3 bg-white border-explorium-green"
        disabled={disabled}
        name="message"
        required
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            const form = e.currentTarget.form;
            if (form) {
              form.requestSubmit();
            }
          }
        }}
      />
      <Button
        onClick={() => {}}
        disabled={disabled}
        variant="cta"
        className="absolute right-2 bottom-2 w-10 h-10 rounded-full"
        type="submit"
      >
        <ArrowRight className="text-black" />
      </Button>
    </form>
  );
}
