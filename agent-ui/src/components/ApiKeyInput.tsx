import { Input } from "@/components/ui/input";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

import { Button } from "@/components/ui/button";
import useExploriumStore from "@/store";
import { ExternalLink, Lock } from "lucide-react";

export default function ApiKeyInput() {
  const setApiKey = useExploriumStore((state) => state.setApiKey);

  return (
    <div className="m-auto flex gap-4 items-start">
      <div className="w-35">
        <h1 className="text-xl font-bold">API Agent</h1>
        <p className="text-sm text-muted-foreground">
          Enter your Explorium API key to start.
        </p>
      </div>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          const form = e.target as HTMLFormElement;
          const apiKey = new FormData(form).get("apiKey") as string;
          setApiKey(apiKey);
        }}
      >
        <div className="flex gap-2 items-center">
          <Input
            name="apiKey"
            placeholder="Enter your API key"
            className="font-mono bg-white w-84"
            type="password"
            required
          />
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <Lock className="w-4 h-4 text-muted-foreground" />
              </TooltipTrigger>
              <TooltipContent align="end">
                <p>We do not store your API key.</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
        </div>
        <div className="flex mt-2 gap-2">
          <Button type="submit" variant="cta">
            Start
          </Button>
          <Button
            className="bg-black text-white cursor-pointer hover:bg-gray-900"
            asChild
          >
            <a
              href="https://developers.explorium.ai/reference/getting_your_api_key"
              target="_blank"
            >
              Get API Access
              <ExternalLink className="w-4 h-4" />
            </a>
          </Button>
        </div>
      </form>
    </div>
  );
}
