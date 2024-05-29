"""The contexts module contains logic for managing the tracing and running of models with :mod:`nnsight.tracing` and :mod:`nnsight.envoy`

The primary two classes involved here are :class:`Tracer <nnsight.contexts.Tracer.Tracer>` and :class:`Invoker <nnsight.contexts.Invoker.Invoker>`.

The :class:`Tracer <nnsight.contexts.Tracer.Tracer>` class creates a :class:`Graph <nnsight.tracing.Graph.Graph>` around the underlying model of an :class:`NNsight <nnsight.models.NNsightModel.NNsight>`. The graph tracks and manages the operations performed on the inputs and outputs of said model.
Module's envoys in the model expose their ``.output`` and ``.input`` attributes which when accessed, add to the computation graph of the tracer.
To do this, they need to know about the current Tracer object, so each module's envoy's ``.tracer`` object is set to be the current Tracer.

The Tracer object also keeps track of the batch_size of the most recent input, the generation index for multi iteration generations, and all of the inputs made during its context in the ``.batched_input`` attribute. Inputs added to this attribute should be in a format where each index is a batch index and allows the model to batch all of the inputs together.

This is to keep things consistent. If two different inputs are in two different valid formats, they both become the same format and are easy to batch.
In the case of LanguageModels, regardless of whether the input are string prompts, pre-processed dictionaries, or input ids, the batched input is only input ids.
On exiting the Tracer context, the Tracer object should use the information and inputs provided to it to carry out the execution of the model.

The :class:`Invoker <nnsight.contexts.Invoker.Invoker>` class is what actually accepts inputs to the model/graph, and it updates its parent Tracer object with the appropriate information about respective inputs. On entering the invoker context with some input, the invoker leverages the model to pre-process and prepare the input to the model. Using the prepared inputs, it updates its Tracer object with a batched version of the input, the size of the batched input, and the current generation index. It also runs a 'meta' version of the input through the model's meta_model. This updates the sizes/dtypes of all of the module's Envoys inputs and outputs based on the characteristics of the input.

nnsight comes with an implementation of a Tracer, Runner,  which enables both local and remote execution.
"""

from .Runner import Runner
