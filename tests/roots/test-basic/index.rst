Test
====

.. toctree::
   :hidden:

   zoom
   empty

.. mermaid::
   :name: test-diagram
   :align: center

   sequenceDiagram
     Alice->>Bob: Hello

.. mermaid::
   :zoom:

   flowchart LR
     A --> B

.. mermaid::
   :caption: My caption text
   :name: captioned-diagram

   flowchart LR
     C --> D

.. mermaid::
   :alt: Sequence diagram of greeting

   sequenceDiagram
     Carol->>Dave: Hi

.. mermaid::
   :config: {"theme": "forest"}

   flowchart LR
     E --> F

.. mermaid::
   :title: My Diagram Title

   flowchart LR
     G --> H
