import asyncio

from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask

from pipecat.transports.local.audio import LocalAudioTransport, LocalAudioTransportParams

async def main():
    # Minimal params. We'll print the signature below if we need to tune device/rate.
    params = LocalAudioTransportParams()

    transport = LocalAudioTransport(params)

    pipeline = Pipeline([
        transport.input(),
        # enhancement stage goes here later (ai-coustics / passthrough)
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
