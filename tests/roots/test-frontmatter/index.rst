Test
====

.. mermaid::

   ---
   title: Auth Flow
   config:
     theme: dark
     look: handDrawn
   ---
   flowchart TD
     A[Login] --> B{Valid?}
     B -->|Yes| C[Dashboard]
     B -->|No| D[Error]
