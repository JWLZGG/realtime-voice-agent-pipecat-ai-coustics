import asyncio

from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask

# Local audio transport (mic + speaker)
from pipecat.transports.local.audio import LocalAudioTransport

async def main():
    transport = LocalAudioTransport(
        input_enabled=True,
        output_enabled=True,
    )

    pipeline = Pipeline([
        transport.input(),
        # enhancer stage goes here later (ai-coustics / passthrough)
        transport.output(),
    ])

    task = PipelineTask(pipeline)
    runner = PipelineRunner()
    await runner.run(task)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped.")
