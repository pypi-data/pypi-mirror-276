depends = ('ITKPyBase', 'MeshToPolyData', 'ITKImageFunction', 'ITKIOMeshBase', 'ITKIOImageBase', 'ITKCommon', )
templates = (  ('WasmImageIO', 'itk::WasmImageIO', 'itkWasmImageIO', True),
  ('WasmImageIOFactory', 'itk::WasmImageIOFactory', 'itkWasmImageIOFactory', True),
  ('WasmMeshIO', 'itk::WasmMeshIO', 'itkWasmMeshIO', True),
  ('WasmMeshIOFactory', 'itk::WasmMeshIOFactory', 'itkWasmMeshIOFactory', True),
)
factories = (("ImageIO","Wasm"),("MeshIO","Wasm"),)
