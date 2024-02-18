import { useRouter } from 'next/router';
import { Flex, Box } from 'reflexbox';

export default function Summary() {
  const router = useRouter();
  const { info } = router.query; // Example: you'll replace this with actual data

  return (
    <Flex flexDirection="column" alignItems="center" justifyContent="center" height="100vh">
      <Box width={[1, 1/2, 1/4]} px={2}>
        <h1>Sunscreen Summary</h1>
        <p>Information: {info}</p>
        {/* Display the actual sunscreen information here */}
      </Box>
    </Flex>
  );
}
